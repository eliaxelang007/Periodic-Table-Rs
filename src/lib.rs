//! This is a chemsistry library for Rust.
//!
//! For now, it only contains constants for each of the elements of the periodic table,
//! but in the future, I'd like it to be able to do calculations on molecules such as
//! determining if they're bonded ionically, covalently, or metalically and finding their
//! molecular masses.
//!
//! Here's a quick example to get you up and running.
//!
//! ```rust
//! /* Note: These snippets are untested */
//! 
//! use periodic_table_rs::HYDROGEN;
//! 
//! fn main() {
//!     println!("{}", HYDROGEN.atomic_mass);
//!     println!("{}", HYDROGEN.boiling_point);
//!     println!("{}", HYDROGEN.density);
//! }
//! ```
//! ```rust
//! /* Or, you can do this. */
//! 
//! use periodic_table_rs::{Element, PERIODIC_TABLE};
//! 
//! fn main() {
//!     const HYDROGEN: Element = PERIODIC_TABLE[0];
//! 
//!     println!("{}", HYDROGEN.atomic_mass);
//!     println!("{}", HYDROGEN.boiling_point);
//!     println!("{}", HYDROGEN.density);
//! }
//! ```

pub mod element;
pub use element::{
    Color, ElectronConfigurationPart, Element, GroupBlock, MatterState, Name, Orbital, Symbol, YearDiscovered,
};

pub mod table;
pub use table::PERIODIC_TABLE;

pub mod elements;
pub use elements::*;
