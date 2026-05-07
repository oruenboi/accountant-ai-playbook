# Legal Normalization Examples

## Bullets
Before:
```
(a) The Licensee must comply.
(b) Payment is due within 30 days.
```
After (`--legal-normalize`):
```
- (a) The Licensee must comply.
- (b) Payment is due within 30 days.
```

## Wrapped bullets
Before (hard-wrapped):
```
- (a) The Licensee must comply with all applicable
  laws and regulations.
```
After (flattened):
```
- (a) The Licensee must comply with all applicable laws and regulations.
```

## Definitions
Before:
```
"Agreement" means this contract between the parties.
```
After:
```
- “Agreement”: this contract between the parties.
```

## Currency highlighting
Before: `A penalty of $10,000 applies.`

After: `A penalty of **$10,000** applies.`

## Notes / caveats
- Avoid enabling `--legal-normalize` on documents where parentheses are used for math or coding; it assumes `(a)`/`(b)` are bullets.
- Currency bolding is regex-based; edge cases like `USD 10,000` are not changed.
