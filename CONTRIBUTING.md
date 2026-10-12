# Contributing to ORBISCOPE

Thanks for your interest in ORBISCOPE.

ORBISCOPE is an independent geospatial intelligence and visual reasoning project. Contributions should make geographic hypotheses more reliable, explainable, reproducible, and useful across different environments.

The guiding principle is simple:

**Evidence over intuition. Reproducibility over anecdotes. Measurable improvements over impressive claims.**

## 1. A geographic clue that transfers

ORBISCOPE benefits from geographic evidence that helps distinguish one location from plausible alternatives.

Useful contributions include:

- Road markings, sign conventions, and infrastructure patterns.
- Architectural styles and regional construction features.
- Vegetation, terrain, and landscape characteristics.
- Publicly documented geographic boundaries and spatial datasets.
- Verified relationships between geographic features.

A useful clue should distinguish a location from its neighbours, not merely describe something common everywhere.

For example, a distinctive road-sign convention supported by an official transportation source is more useful than a generic observation that a photograph contains trees.

### Contribution requirements

Every documented clue should include:

1. **Observation:** What is visible or measurable?
2. **Geographic scope:** Where is the clue applicable?
3. **Evidence:** A reliable public source or appropriately licensed observation.
4. **Limitations:** Where might the clue fail or produce false positives?
5. **Verification:** A reproducible example, test, or documented validation method where applicable.

Keep globally applicable observations separate from country- or region-specific evidence.

Proposed organization:

```text
references/
├── clues/
│   ├── README.md
│   ├── global.md
│   └── regions/
│       ├── in.md
│       └── us.md
└── data-sources.md
```

These paths describe the intended structure and should be created as the corresponding functionality is implemented.

Do not turn a single landmark, an unsupported assumption, or a coincidental visual resemblance into a general geographic rule.

## 2. A geographic dataset or regional reference

Regional datasets can improve candidate generation and verification without complicating the core reasoning pipeline.

Useful contributions include:

- Administrative boundaries.
- Public road and place-name datasets.
- Coordinate reference system definitions.
- Verified geographic lookup tables.
- Publicly documented regional infrastructure patterns.
- Elevation and terrain data with suitable licensing.

Proposed organization:

```text
data/
├── sources/
├── boundaries/
├── elevation/
└── lookups/
```

### Dataset requirements

Every contributed dataset must document:

- **Source:** Original publisher and source URL.
- **Coverage:** Geographic extent and any excluded areas.
- **Collection date:** When the data was obtained.
- **License:** Terms governing redistribution and use.
- **Schema:** Field names, data types, units, and coordinate systems.
- **Limitations:** Missing records, positional uncertainty, or known coverage gaps.
- **Validation:** Checks that detect malformed, duplicated, or inconsistent records.

Prefer official and authoritative sources where available. Do not commit large generated datasets, credentials, private API responses, or files that cannot legally be redistributed.

For external services, document rate limits, attribution requirements, caching behaviour, and fallback behaviour. Keep provider-specific logic separate from the geographic reasoning core.

If a dataset requires new processing logic, contribute the dataset and algorithmic changes separately whenever practical.

## 3. A change to the core algorithms

Core changes affect the reliability of ORBISCOPE's visual analysis, geographic search, terrain analysis, geometric reasoning, candidate ranking, or reporting.

Examples include improvements to:

- Image feature extraction.
- Camera orientation and geometric estimation.
- Terrain-profile matching.
- Geographic candidate generation.
- Candidate scoring and uncertainty estimation.
- Coordinate transformations.
- Evidence reporting and failure diagnostics.

Open a focused pull request and include four things.

### 3.1 The failure

Show a concrete case where the existing implementation produces an incorrect result, cannot distinguish plausible candidates, or fails to complete.

Include the relevant input, expected behaviour, actual output, and the first stage where the result becomes incorrect.

Use a photograph you took yourself or one whose photographer has explicitly agreed to its use.

### 3.2 A general solution

Explain why the change should work across a class of inputs rather than one carefully selected example.

Avoid hard-coded locations, image-specific thresholds, and parameters tuned exclusively to the demonstration case.

If the change introduces a new parameter, a more permissive filter, or an alternative algorithm, document its default, bounds, and effect on existing behaviour. Preserve a way to compare against the previous method when practical.

### 3.3 Before and after

Provide a reproducible evaluation that includes:

- The test input and its provenance.
- The baseline output.
- The modified output.
- The metric used to compare them.
- The command needed to reproduce the comparison.

Use appropriate metrics for the change. Depending on the component, these might include geographic distance error, candidate recall, ranking quality, geometric residuals, runtime, or failure rate.

Never present a lower geometric residual as proof of a correct location by itself. A better numerical fit is useful only when interpreted alongside geographic plausibility and independent evidence.

### 3.4 Regression checks

Demonstrate that the change does not undermine unrelated cases.

Include:

- A focused unit test.
- A regression test for the original failure.
- Tests covering relevant edge cases.
- An evaluation on inputs that were not used to develop the change, where a suitable test set exists.

Keep evaluation data and scripts reproducible. If a result depends on external services, document the dependency and provide an offline test path where practical.

## 4. A run that went wrong

Incorrect results are valuable when they help identify where the reasoning pipeline failed.

Open an issue containing as much of the following as you can safely share:

1. **Input:** A photograph you took or are authorized to use, or a description if you cannot share it.
2. **Expected result:** The known location or expected behaviour, if verified.
3. **Actual result:** The candidates, ranking, confidence information, or error message produced.
4. **First failure:** The earliest pipeline stage where the output diverged from the expected result.
5. **Environment:** Operating system, Python version, relevant dependency versions, and the command used.
6. **Reproduction:** Minimal steps that another contributor can follow.

If the failure involves external data, identify the provider and whether the problem appears to be a timeout, unavailable coverage, rate limit, stale data, or a reasoning error.

Remove API keys, access tokens, private filesystem paths, personal information, and other sensitive details before posting logs.

Do not share someone else's private photographs or attempt to identify a private individual or residence.

## 5. Code and repository standards

Keep contributions small enough to review and clear enough to reproduce.

- **One focused change per pull request.** Separate unrelated refactors from algorithmic changes.
- **Explicit dependencies.** Declare dependencies in the project's package configuration rather than relying on an undeclared local environment.
- **Deterministic tests.** Unit tests should not require live geographic services or network access.
- **Clear interfaces.** Keep image processing, geographic data access, geometry, ranking, and reporting responsibilities separate.
- **Traceable results.** Where practical, preserve the evidence and intermediate measurements that explain a candidate's score.
- **Honest uncertainty.** Do not present heuristic rankings as calibrated probabilities unless calibration has been measured.
- **Reproducible data.** Record dataset provenance, licensing, and processing steps.
- **Readable documentation.** Explain why a method exists, its assumptions, and when it can fail.

Follow the formatting, naming, and testing conventions already established in the relevant part of the repository. If those conventions have not yet been established, propose a simple convention with the change rather than introducing a large framework unnecessarily.

### Intended architecture

The following is the planned separation of responsibilities, not a claim that every module already exists.

```text
src/orbiscope/
├── ingestion/    # Input validation and image preparation
├── vision/       # Visual features and image analysis
├── geospatial/   # Geographic datasets and spatial queries
├── terrain/      # Elevation and terrain-profile analysis
├── geometry/     # Camera, projection, and geometric reasoning
├── ranking/      # Candidate scoring and comparison
└── reporting/    # Evidence, uncertainty, and result summaries

tests/
examples/
docs/
references/
data/
```

Place new functionality where its primary responsibility belongs. Avoid making the reporting layer responsible for geographic queries or embedding provider-specific behaviour throughout the algorithmic code.

## 6. Testing and validation

Use the project's configured test runner and documented development commands. The following commands are intended once the corresponding configuration and tests have been added:

```bash
# Install the project and development dependencies
uv sync --dev

# Run the test suite
uv run pytest

# Run a focused test
uv run pytest tests/path_to_test.py -q

# Check the patch
git diff --check
```

Replace the example test path with the actual test file.

Tests should not depend on downloading large machine-learning models, accessing live APIs, or uploading photographs unless the test explicitly targets that integration and the dependency is documented.

For external integrations, mock service responses in unit tests and keep live connectivity checks separate from offline regression checks.

Before opening a pull request, confirm that:

- [ ] The change has a clear purpose and scope.
- [ ] Relevant tests pass.
- [ ] New behaviour has regression coverage.
- [ ] Data sources and licenses are documented.
- [ ] Documentation reflects actual implementation.
- [ ] No secrets, private photographs, or generated artifacts were committed.
- [ ] The change can be reproduced by another contributor.

## 7. Privacy, responsible use, and licensing

ORBISCOPE should support geographic reasoning without becoming a tool for exposing private individuals or targeting sensitive locations.

Contributions must not introduce:

- Personal identification or face-matching functionality.
- Private-home identification workflows targeting individuals.
- Non-consensual tracking or surveillance features.
- Personal information extracted from images without an appropriate basis.
- Unauthorized access to geographic services or datasets.

Use photographs you created yourself or have permission to use. Respect dataset licenses, attribution requirements, copyright, privacy, and applicable law.

Do not commit private source photographs or their metadata by default. Use synthetic, public-domain, appropriately licensed, or consented test inputs where possible.

The repository's selected license governs contributions to the code. Data and photographs may have different licensing requirements and must be documented independently. If a contribution requires a new license or redistribution permission, resolve that before merging it.

## 8. Documentation and project claims

Documentation is part of the engineering work.

Every documented feature should map to an implementation, a reproducible command, or a clearly labeled design proposal.

- Label planned features as planned.
- Link documented commands to the scripts or configuration that implement them.
- Support performance claims with reproducible measurements.
- State the geographic coverage and limitations of any evaluation dataset.
- Distinguish a candidate ranking from a verified location.
- Keep examples consistent with the current interfaces.

Do not invent benchmark results, claim unimplemented capabilities, or imply that a demonstration proves general accuracy.

When an algorithm changes, update its explanation, assumptions, limitations, and relevant examples alongside the code.

## 9. Pull request process

1. Open an issue first for substantial architectural changes.
2. Create a focused branch from the current default branch.
3. Implement the change with tests and documentation.
4. Run the relevant checks locally.
5. Open a pull request describing the motivation, approach, validation, and limitations.
6. Respond to review feedback and update the tests when the implementation changes.

For small documentation corrections, an issue is not required.

A good pull request explains not only what changed, but also what evidence shows the change is an improvement.

## 10. Questions and discussions

For bugs, use the issue tracker and include reproducible details.

For feature proposals, explain the problem, the intended users, alternative approaches considered, and the expected trade-offs before proposing a large implementation.

For security or privacy concerns, avoid posting sensitive details publicly.

Thank you for helping make ORBISCOPE more rigorous, transparent, and reproducible.

**ORBISCOPE**

*OBSERVE · LOCALIZE · VERIFY.*