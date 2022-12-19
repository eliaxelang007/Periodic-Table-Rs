//! A Rust library that takes the elements of the periodic table and turns
//! them into Rust structs.
//!
//! I've made the element's names, symbols, states of matter, group blocks, and more
//! into enums among other things that (hopefully) make this library as easy to use as
//! possible.
//!
//! Here's the Element struct's definition:
//!
//! ```rust
//! pub struct Element {
//!     pub atomic_number: u8,
//!     pub symbol: Symbol,
//!     pub name: Name,
//!     pub atomic_mass: f64,
//!     pub cpk_hex_color: Option<Color>,
//!     pub electron_configuration: &'static [ElectronConfigurationPart],
//!     pub electronegativity: Option<f64>,
//!     pub atomic_radius: Option<u16>,
//!     pub ionization_energy: Option<f64>,
//!     pub electron_affinity: Option<f64>,
//!     pub oxidation_states: Option<&'static [i8]>,
//!     pub standard_state: MatterState,
//!     pub melting_point: Option<f64>,
//!     pub boiling_point: Option<f64>,
//!     pub density: Option<f64>,
//!     pub group_block: GroupBlock,
//!     pub year_discovered: YearDiscovered,
//! }
//! ```
//!

pub mod element;
pub use element::{
    Color, ElectronConfigurationPart, Element, GroupBlock, MatterState, Name, Orbital, Symbol, YearDiscovered,
};

pub mod table;
pub use table::PERIODIC_TABLE;

pub mod elements;
pub use elements::*;
