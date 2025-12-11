# Comprehensive Test Case Documentation and Coverage Strategy

## Plan Overview

Draft a systematic approach to identify, document, and implement comprehensive test cases covering 100% of code logic and edge cases.

## Steps

1. **Create test case inventory document** in [.github/TEST_CASES.md](.github/TEST_CASES.md) organized by service/feature with categories: Happy Path, Edge Cases, Error Handling, and Concurrency.

2. **Document TaskItem scoring edge cases**: Test all combinations of Priority (negative, 0, 1-3, >3), Status (pending, in-progress, completed, invalid), Age (0, 7, 14, 30 days), IsCompleted flag, and title word length.

3. **Document InMemoryTaskService tests**: Cover ID generation thread-safety, concurrent operations, null/empty collections, and boundary conditions (max int ID, duplicate operations).

4. **Document CsvTaskService tests**: Cover file I/O (missing file, permission denied, corrupted CSV), CSV escaping (quotes, commas, newlines in values), concurrent file access, and recovery scenarios.

5. **Document API endpoint tests**: Integration tests for all 5 endpoints (GET all, GET by ID, POST create, PUT update, DELETE), status query filtering, response codes, null validations, and request body validation.

6. **Document validation tests**: Null/empty title handling, negative/zero priority values, invalid status strings, and edge case date values.

7. **Organize by test class**: Map each test case to the appropriate xUnit test class (create new ones for gaps).

## Further Considerations

### 1. Test Case Taxonomy
Question: Should the document group tests by (A) service/component, (B) test type (unit/integration/edge-case), or (C) risk area (data integrity, performance, concurrency)?

**Recommendation**: Use (A) with subsections for test types.

### 2. Coverage Metrics
Would you like the document to include coverage % targets per service and a checklist to track implementation progress?

### 3. CSV File Handling Scope
CsvTaskService has no tests currently. Should this get the same depth of testing as InMemoryTaskService, or a focused subset given it's for persistence demonstration?

## Key Findings from Analysis

### Current Test Coverage Status
- **InMemoryTaskService**: 7 tests covering basic CRUD operations
- **TaskItem.GetScore()**: 7 tests covering priority/status combinations
- **CsvTaskService**: Zero tests (gap)
- **API Endpoints**: Zero tests (gap)
- **Validation**: Zero tests (gap)
- **Concurrency**: Zero tests (gap)

### Critical Areas Requiring Test Coverage

#### TaskItem.GetScore() Edge Cases
- Priority values: negative, 0, 1, 2, 3, >3
- Status values: "pending", "in-progress", "completed", invalid/custom
- Age-based escalation: 0, 7, 14, 30+ days old
- Title analysis: word length variations, empty title, very long title
- IsCompleted flag combinations with each status
- Score floor validation (Math.Max(0, ...))

#### InMemoryTaskService
- **ID Generation**: Thread-safe increment, max int boundary
- **Concurrent Operations**: Multiple threads reading/writing simultaneously
- **Edge Collections**: Empty list operations, single item, duplicate creates
- **Update/Delete**: Non-existent IDs, null taskItem parameter
- **GetAll with Filtering**: Status query parameter case sensitivity

#### CsvTaskService (Persistence Layer)
- **File Operations**: Missing file, read-only file, no disk space
- **CSV Escaping**: Titles with commas, quotes, newlines, special characters
- **Data Corruption**: Malformed CSV, invalid record format, incomplete rows
- **Concurrent Access**: Multiple processes reading/writing file simultaneously
- **State Management**: ID counter persistence, recovery from crashes
- **Large Files**: Performance with 1000+, 10000+ records

#### API Endpoints
- **GET /tasks**: Returns all tasks, empty collection, large result sets
- **GET /tasks?status=X**: Case sensitivity, non-existent status, empty result
- **GET /tasks/{id}**: Valid ID, invalid ID, negative ID, max int ID
- **POST /tasks**: Valid creation, null/empty title, all fields, minimal fields
- **PUT /tasks/{id}**: Valid update, invalid ID, partial update, null values
- **DELETE /tasks/{id}**: Valid delete, invalid ID, delete non-existent

#### Input Validation
- Null or empty Title field
- Negative, zero, and extreme priority values
- Invalid status strings
- Future-dated CreatedAt values
- Unicode/special characters in title and description

#### Error Handling & Recovery
- File I/O errors in CSV service
- Concurrent modification exceptions
- Invalid request bodies
- Missing or malformed JSON
- Network timeouts (if applicable)

#### Performance & Boundary Conditions
- Very large task lists (10000+ items)
- Very long titles/descriptions
- Rapid concurrent operations
- Repeated operations on same task

## Test Organization Structure

```
DotnetApp.Tests/
├── Models/
│   └── TaskItemTest.cs (EXISTING - expand)
│       ├── GetScore_Priority_* (existing 7 tests)
│       └── [ADD] Edge cases, boundaries, status variations
├── Services/
│   ├── InMemoryTaskServiceTests.cs (EXISTING - expand)
│   │   ├── CRUD operations (existing 7 tests)
│   │   └── [ADD] Concurrency, edge cases, filtering
│   └── CsvTaskServiceTests.cs (NEW)
│       ├── File I/O operations
│       ├── CSV escaping
│       ├── Concurrent access
│       └── Recovery scenarios
└── Integration/
    └── TaskApiEndpointTests.cs (NEW)
        ├── GET /tasks
        ├── GET /tasks?status=X
        ├── GET /tasks/{id}
        ├── POST /tasks
        ├── PUT /tasks/{id}
        └── DELETE /tasks/{id}
```

## Implementation Priority

**Phase 1 (Critical Path)**: TaskItem edge cases + API endpoints
- Covers core business logic and HTTP contract
- Easiest to implement without infrastructure changes

**Phase 2 (Data Integrity)**: CsvTaskService + Validation
- Ensures persistence layer reliability
- Validates data correctness

**Phase 3 (Robustness)**: Concurrency + Error scenarios
- Stress tests and failure modes
- Production readiness

## Success Criteria

- [ ] All test cases documented in TEST_CASES.md
- [ ] Coverage report shows >90% line coverage
- [ ] All identified edge cases have corresponding tests
- [ ] All critical gaps filled with tests
- [ ] Documentation includes implementation checklist
