# Copilot instructions for dukit

## Writing/extending qlang tests (`tests/qlang/`)

When adding or improving tests for qlang symbols/operators (getters, setters,
stylers, etc.), follow the conventions already established in
`tests/qlang/op_getters/test_rows.py` — treat it as the canonical template.
Prefer this over inventing a new/simpler pattern per file.

Key points:

- **Isolate the operator under test; don't route through an unrelated
  operator.** To make a getter's row/col/val selection observable, use a
  dedicated trim/selection getter (e.g. `%%:trim` / `%:trim` via
  `GetTrimmedSelection`) so the expected result is a plain, untouched slice
  of `get_df()` (e.g. `df.loc[[1, 4, 10], ['age']]`). Avoid piggybacking a
  setter (e.g. `%%%=X`) just to "see" the selection — that couples two
  operators together, forces dtype workarounds (`.convert_dtypes()` /
  `.astype('object')`) to match engine output, and tests the setter as much
  as the getter.
- **Structure: `params` list of `(code, expected, message)` tuples +
  `@pytest.mark.parametrize`.** Group related cases into one parametrized
  test function per topic (e.g. `test_dates`, `test_numeric`, `test_regex`,
  `test_typechecks`, `test_typeflags`, `test_uniqueness`), not one bespoke
  function per operator/case.
- **Use the `check_message(expected_strings)` helper** (reading `log()`)
  when a case should also assert on logged warnings/errors; pass `None` in
  the tuple when there's nothing to check.
- **Cover breadth, not just the happy path**: for each operator also
  include, where applicable — negated forms (`!:isstr()`, `:!isna()`),
  `+strict` variants, AND/OR combinators (`&&!:isna()`, `//:isyn()`),
  literal/date-format variants, regex equality/search (`==(... +regex)`,
  `?(... +regex)`), and type-coercion flags (`+int`/`+float`/`+num`/`+str`).
- **Cross-reference known-good expected indices** from sibling test files
  (e.g. `test_rows.py`) instead of re-deriving them from scratch, when the
  same column/condition is exercised at a different scope — getter
  functions operate per-column-`Series`, so results are identical across
  scopes when only one column is selected.
- **Place tests by operator category, not by symbol module.** Getter
  behavior tests belong in `tests/qlang/op_getters/`, setter behavior tests
  in `tests/qlang/op_setters/`, matching the scope the code exercises
  (cols/rows/vals) — not in a catch-all file like `test_symbols.py`.
  Reserve `test_symbols.py`-style files for things that aren't
  getter/setter behavior (e.g. parsing/alias/token-level checks).
- Environment note: `pytest --cov` / multi-file coverage runs can fail here
  with `ImportError: cannot load module more than once per process` (numpy
  re-import quirk). Run tests with `-p no:cov` when validating across
  `tests/qlang`, and prefer reading an existing HTML coverage report under
  `tests/coverage/` over re-running coverage tooling if one is available.
- **Before writing new tests, check whether the behavior is already covered**
  elsewhere (e.g. `op_setters/test_vals.py`, `op_getters/test_rows.py`,
  `test_basics.py`) to avoid duplicating coverage. Only add tests for
  genuinely untested combinations of scope/operator/flags.
- **Gotcha**: if a new test file shares a basename with one in a sibling
  folder (e.g. `op_getters/test_vals.py` and `op_setters/test_vals.py`),
  pytest's default import mode fails to collect both with
  `import file mismatch`. Fix by adding an empty `__init__.py` to each
  `tests/qlang/op_getters/` and `tests/qlang/op_setters/` folder (already
  done) rather than renaming files to avoid the collision.

### qlang scope/query mental model (needed to write correct test code)

- `%` = cols scope, `%%` = rows scope, `%%%` = vals scope. Each also has an
  AND-connector variant (`&`/`&&`/`&&&`) and an OR-connector variant
  (`/`/`//`/`///`) for combining conditions within the same scope.
  - Bare literals default to **cols** scope.
  - Bare getter symbols (no preceding scope token) default to **rows** scope via `_preparse_for_getter`.
  - Bare setter/styler symbols default to **vals** scope via `_preparse_for_setter_or_styler`.
  - Bare scope tokens with no operator (e.g. trailing `%%%`) infers a `GetAll` operator — used to "reset" the selection. e.g. `age %%<0  =X  %%`.
- `_get_vals` requires both `mask_cols` and `mask_rows` to be non-empty, or it logs an error and returns the query unchanged 
- Getter `.getter()` methods operate purely on a per-column `pd.Series`, so when only one column is selected, rows-scope (`%%`) and vals-scope (`%%%`) getters produce identical per-cell boolean masks — safe to derive one scope's expected results from another's already-validated test data.
- `get_df()` (in `src/dukit/pandas.py`) is the canonical sample dataframe
  used by nearly all qlang tests; it's deliberately messy (mixed types,
  NA/NK/date variants per column) — inspect its raw values directly rather
  than assuming clean data when deriving expected results.

## Docstring conventions

When writing or updating docstrings across the project, follow the style used
by the current public APIs, especially `src/dukit/diffing.py`:

- Start descriptive lines with lowercase letters, including continuation lines
  after section headers. Keep standard NumPy-style section headers such as
  `Parameters`, `Returns`, `Raises`, `Examples`, and `Notes` unchanged.
- Use `df` instead of `DataFrame` in descriptive prose, and use `col`/`cols`
  instead of `column`/`columns`. Preserve technical type expressions such as
  `pandas.DataFrame` where they identify a return type.
- Use NumPy-style sections for public functions and methods. Document
  parameters with their type and default, then document `Returns` and
  `Raises` where applicable.
- Keep descriptions concise and behavior-focused. Document accepted values,
  defaults, side effects, and important edge cases rather than repeating the
  implementation.
- Use cross-references such as `:func:`diff`` and ``:class:`Diff``` when a
  related public API is already documented.
- Include short doctest examples for user-facing functions when an example
  clarifies the normal workflow.
