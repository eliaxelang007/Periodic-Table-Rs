
## About

This is a Rust library for chemistry.

## Installation

* Install this package from [crates.io](https://crates.io/crates/periodic-table-rs).

## Usage

Here's some sample code that shows how you can get the atomic mass, boiling point, and density of hydrogen. 

```rust
/* Note: These snippets are untested */

use periodic_table_rs::HYDROGEN;

fn main() {
    println!("{}", HYDROGEN.atomic_mass);
    println!("{}", HYDROGEN.boiling_point);
    println!("{}", HYDROGEN.density);
}
```
```rust
/* Or, you can do this. */

use periodic_table_rs::{Element, PERIODIC_TABLE};

fn main() {
    const HYDROGEN: Element = PERIODIC_TABLE[0];

    println!("{}", HYDROGEN.atomic_mass);
    println!("{}", HYDROGEN.boiling_point);
    println!("{}", HYDROGEN.density);
}
```

## Documentation

The documentation for this project is in its [crates.io](https://crates.io/crates/periodic-table-rs) page.
[Here's a quick link to it.](https://docs.rs/periodic-table-rs/latest/periodic_table_rs/index.html)

## Additional information

The element data in this library primarily came from [PubChem](https://pubchem.ncbi.nlm.nih.gov/periodic-table/) with some of its missing fields filled in by the data from the [Royal Society of Chemistry](https://www.rsc.org/periodic-table). 

The combined and parsed element data from both these sources is in [this json file](https://github.com/eliaxelang007/Periodic-Table-Rs/blob/master/_data_formatting/final.json) and you can use it in your own projects if all you need is the raw element data :D