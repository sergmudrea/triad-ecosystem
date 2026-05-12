markdown

# TRIAD Architecture Documentation

## Overview

TRIAD is a closed-loop ecosystem of three autonomous agent types:

- **BLACK**: Predator — scans, attacks, mutates on failure
- **RED**: Supervisor — defines evolution parameters, measures fitness, makes decisions
- **BLUE**: Defender — patches, optimizes memory, replicates improvements

## Core Components

### 1. Meta-Memory

Self-optimizing distributed memory pool with:

- **Encryption**: AES-256 with automatic key rotation
- **Compression**: LZ4 frame compression
- **Deduplication**: SHA-256 checksum based
- **Indexing**: Bloom filters + hash indexes
- **TTL**: Automatic expiration of old records

### 2. Replication Engine

Pub/sub pattern for optimization distribution:

- Subscribers: Black, Red, Blue agents
- Broadcasts: Memory optimizations, parameter updates
- Retry logic: 3 attempts, 30 second timeout

### 3. Evolution Parameters

Red-defined parameters controlling evolution:

| Category | Parameters |
|----------|------------|
| Mutation | min/max/initial rate, dynamic adjustment |
| Fitness | thresholds (cull/keep/promote), weights |
| Population | min/max size, elitism, selection pressure |
| Time | generation age, starvation days |

### 4. Decision Engine

Red's autonomous decision logic:

if fitness < cull_threshold → CULL
elif fitness < keep_threshold → MUTATE
elif fitness >= promote_threshold → PROMOTE
elif population < min → CREATE_NEW
elif generation_age > max → ROTATE
text


### 5. Advanced Features

- **Novelty Search**: Rewards behavioral diversity
- **MAP-Elites**: Quality-diversity archive
- **Coevolution**: Black vs Blue arms race

## Data Flow

┌─────────────────────────────────────────────────────────────────┐
│ META-MEMORY │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │Encrypted│ │Compressed│ │Deduped │ │Indexed │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
▲ ▲ ▲
│ │ │
┌────┴────┐ ┌─────┴─────┐ ┌───┴────┐
│ BLACK │ │ RED │ │ BLUE │
│ writes │ │ reads/ │ │ writes │
│ successes│ │ writes │ │ optims │
└─────────┘ └───────────┘ └────────┘
text


## State Machines

### Black Agent States

INIT → SCANNING → ATTACKING → [SUCCESS → RECORD] / [FAILURE → MUTATE] → REPEAT
text


### Red Agent States

INIT → SUPERVISING → MEASURING → DECIDING → [MUTATE|CULL|PROMOTE|CREATE] → REPEAT
text


### Blue Agent States

INIT → ADAPTING → OPTIMIZING → REPLICATING → CLEANING → REPEAT
text


## Communication Patterns

1. **Memory-based**: Agents communicate via shared Meta-Memory
2. **Pub/Sub**: Replication engine broadcasts optimizations
3. **Command queue**: Red sends mutation/cull commands to Black

## Performance Considerations

- Meta-memory operations are O(log n) with indexes
- Replication is asynchronous, non-blocking
- Agent loops are independent, run concurrently
- Redis persistence optional, can be disabled for speed

## Security & Isolation

- All execution in sandboxed environment
- No external network access
- Encrypted memory at rest
- Input validation on all commands
