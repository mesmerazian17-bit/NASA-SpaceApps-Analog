# Earth–Moon–Mars Feature Contract v0.1

## Purpose
Common input structure for the planetary analog matching engine.

## Files
- `earth_moon_feature_schema.json`: JSON Schema validation contract.
- `earth_moon_feature_example.json`: illustrative record template.

## Rules
1. Preserve original physical values and units.
2. Do not substitute normalized values for raw measurements.
3. Unknown measurements must be represented as null.
4. Record missing features in `quality.missing_features`.
5. Record source and calculation information in `feature_metadata`.
6. Comparability must be explicitly classified:
   - comparable
   - approximate
   - unavailable
   - requires_review
7. Do not calculate scientific similarity scores in this input contract.
8. Do not assume Earth and lunar measurements are equivalent merely
   because they share a field name.
9. Roughness and normalization definitions require scientific review
   by Member 4 before cross-planet scoring.

## Important
The example is a template, not an approved scientific dataset.
Do not feed it into production matching as measured data.
