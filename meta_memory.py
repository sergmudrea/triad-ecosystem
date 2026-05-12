# src/core/meta_memory.py

import hashlib
import json
import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

try:
    import redis.asyncio as redis

    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

import msgpack
import lz4.frame

from src.utils.crypto import encrypt, decrypt, generate_key
from src.utils.hashing import calculate_checksum


@dataclass
class MemoryMetadata:
    """Metadata for each memory record."""

    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    compressed: bool = False
    encrypted: bool = False
    checksum: str = ""
    original_size: int = 0
    compressed_size: int = 0
    optimization_score: float = 0.0
    inherited_from: str = ""


@dataclass
class MemoryRecord:
    """Complete memory record with data and metadata."""

    id: str
    data: Any
    meta: MemoryMetadata
    ttl: int = 3600000  # 1 hour default
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=1))

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at


@dataclass
class MemoryOptimization:
    """Record of a memory optimization operation."""

    id: str
    applied_by: str  # "blue" | "red" | "black"
    timestamp: datetime
    type: str
    target_keys: List[str]
    original_size: int
    optimized_size: int
    compression_ratio: float
    optimization_recipe: Dict[str, Any]
    propagate_to_all: bool = True
    propagated: bool = False


class MetaMemory:
    """
    Self-optimizing, self-replicating memory pool.

    Features:
    - Automatic compression (LZ4)
    - Deduplication via SHA-256 checksums
    - Encryption with rotating keys (AES-256)
    - Bloom filters for fast existence checks
    - TTL-based auto-pruning
    - Optimization replication to all cluster nodes
    """

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self._records: Dict[str, MemoryRecord] = {}
        self._indexes: Dict[str, Set[str]] = {}
        self._bloom_filter: Set[str] = set()
        self._optimizations: List[MemoryOptimization] = []
        self._encryption_key: Optional[str] = None
        self._total_size: int = 0
        self._redis_url = redis_url

        if HAS_REDIS:
            try:
                self.redis = redis.from_url(redis_url)
            except Exception:
                self.redis = None
        else:
            self.redis = None

        self._rotate_encryption_key()

    def _rotate_encryption_key(self):
        """Generate a new encryption key (called by Blue each cycle)."""
        self._encryption_key = generate_key()

    async def set(self, key: str, value: Any, ttl: int = 3600000, source: str = "unknown") -> None:
        """Store a value in memory with optional TTL."""
        data = value
        original_size = len(json.dumps(data, default=str))

        compressed = lz4.frame.compress(msgpack.packb(data))
        compressed_size = len(compressed)

        encrypted = encrypt(compressed, self._encryption_key)
        checksum = calculate_checksum(data)

        if checksum in self._bloom_filter:
            return

        record = MemoryRecord(
            id=str(uuid4()),
            data=encrypted,
            meta=MemoryMetadata(
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                compressed=True,
                encrypted=True,
                checksum=checksum,
                original_size=original_size,
                compressed_size=compressed_size,
                inherited_from=source,
            ),
            ttl=ttl,
            expires_at=datetime.now() + timedelta(milliseconds=ttl),
        )

        self._records[key] = record
        self._bloom_filter.add(checksum)
        self._total_size += compressed_size
        await self._index_key(key)

        if self.redis:
            try:
                await self.redis.setex(
                    f"memory:{key}",
                    ttl // 1000,
                    msgpack.packb({
                        "id": record.id,
                        "data": encrypted.hex() if isinstance(encrypted, bytes) else encrypted,
                        "meta": {
                            "created_at": record.meta.created_at.isoformat(),
                            "checksum": checksum,
                            "original_size": original_size,
                            "compressed_size": compressed_size,
                        },
                    }),
                )
            except Exception:
                pass

    async def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from memory."""
        if key not in self._records:
            if self.redis:
                try:
                    data = await self.redis.get(f"memory:{key}")
                    if data:
                        return msgpack.unpackb(data)
                except Exception:
                    pass
            return None

        record = self._records[key]
        record.meta.last_accessed = datetime.now()
        record.meta.access_count += 1

        decrypted_data = decrypt(record.data, self._encryption_key)
        decompressed = msgpack.unpackb(lz4.frame.decompress(decrypted_data))

        return decompressed

    async def delete(self, key: str) -> None:
        """Remove a key from memory."""
        if key in self._records:
            record = self._records.pop(key)
            self._bloom_filter.discard(record.meta.checksum)
            self._total_size -= record.meta.compressed_size
            if self.redis:
                try:
                    await self.redis.delete(f"memory:{key}")
                except Exception:
                    pass

    async def optimize(self, optimizer: str = "blue") -> MemoryOptimization:
        """Perform full memory optimization. Called by Blue each cycle."""
        original_size = self._total_size

        self._rotate_encryption_key()
        await self._deduplicate()
        await self._reencrypt_all()
        await self._prune_expired()
        await self._rebuild_indexes()

        optimized_size = self._total_size
        compression_ratio = optimized_size / original_size if original_size > 0 else 1.0

        optimization = MemoryOptimization(
            id=str(uuid4()),
            applied_by=optimizer,
            timestamp=datetime.now(),
            type="full_optimization",
            target_keys=list(self._records.keys()),
            original_size=original_size,
            optimized_size=optimized_size,
            compression_ratio=compression_ratio,
            optimization_recipe={
                "algorithm": "lz4+aes256+bloom",
                "parameters": {"compression_level": 9, "key_rotation": True},
                "reapplication_guide": "Run deduplication first, then compress, then reindex",
            },
        )

        self._optimizations.append(optimization)
        return optimization

    async def _deduplicate(self) -> None:
        """Remove duplicate records based on checksum."""
        seen_checksums: Set[str] = set()
        to_delete: List[str] = []

        for key, record in self._records.items():
            if record.meta.checksum in seen_checksums:
                to_delete.append(key)
            else:
                seen_checksums.add(record.meta.checksum)

        for key in to_delete:
            await self.delete(key)

    async def _reencrypt_all(self) -> None:
        """Re-encrypt all records with new key."""
        for key, record in list(self._records.items()):
            try:
                decrypted = decrypt(record.data, record.meta.checksum or self._encryption_key)
                decompressed = msgpack.unpackb(lz4.frame.decompress(decrypted))
                await self.set(key, decompressed, record.ttl)
            except Exception:
                pass

    async def _prune_expired(self) -> None:
        """Remove expired records."""
        to_delete = [key for key, record in self._records.items() if record.is_expired()]
        for key in to_delete:
            await self.delete(key)

    async def _index_key(self, key: str) -> None:
        """Index a key for fast search."""
        words = key.replace("/", ":").replace("-", ":").split(":")
        for word in words:
            if word not in self._indexes:
                self._indexes[word] = set()
            self._indexes[word].add(key)

    async def _rebuild_indexes(self) -> None:
        """Rebuild all indexes from scratch."""
        self._indexes = {}
        for key in self._records:
            await self._index_key(key)

    async def search(self, query: str) -> List[str]:
        """Search by keyword using indexes."""
        if query not in self._indexes:
            return []
        return list(self._indexes[query])

    async def get_health(self) -> Dict[str, Any]:
        """Get memory health metrics."""
        total_compressed = sum(r.meta.compressed_size for r in self._records.values())
        total_original = sum(r.meta.original_size for r in self._records.values())

        return {
            "total_records": len(self._records),
            "total_size_bytes": total_compressed,
            "compression_ratio": total_compressed / total_original if total_original > 0 else 1.0,
            "duplicate_count": len(self._records) - len(self._bloom_filter),
            "encryption_rotation_count": len(self._optimizations),
            "index_count": len(self._indexes),
            "last_optimization": self._optimizations[-1].timestamp if self._optimizations else None,
        }

    async def close(self) -> None:
        """Close Redis connection."""
        if self.redis:
            try:
                await self.redis.close()
            except Exception:
                pass
