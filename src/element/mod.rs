pub mod names;
pub use names::Name;

pub mod symbols;
pub use symbols::Symbol;

#[derive(Debug)]
pub struct Element {
    pub atomic_number: u8,
    pub symbol: Symbol,
    pub name: Name,
    pub atomic_mass: f64,
    pub cpk_hex_color: Option<Color>,
    pub electron_configuration: &'static [ElectronConfigurationPart],
    pub electronegativity: Option<f64>,
    pub atomic_radius: Option<u16>,
    pub ionization_energy: Option<f64>,
    pub electron_affinity: Option<f64>,
    pub oxidation_states: Option<&'static [i8]>,
    pub standard_state: MatterState,
    pub melting_point: Option<f64>,
    pub boiling_point: Option<f64>,
    pub density: Option<f64>,
    pub group_block: GroupBlock,
    pub year_discovered: YearDiscovered,
}

#[derive(Debug)]
pub enum MatterState {
    Gas,
    Solid,
    Liquid,
}

#[derive(Debug)]
pub enum GroupBlock {
    Nonmetal,
    NobleGas,
    AlkaliMetal,
    AlkalineEarthMetal,
    Metalloid,
    Halogen,
    PostTransitionMetal,
    TransitionMetal,
    Lanthanide,
    Actinide,
}

#[derive(Debug)]
pub struct Color {
    pub red: u8,
    pub green: u8,
    pub blue: u8,
}

#[derive(Debug)]
pub enum Orbital {
    S,
    P,
    D,
    F,
}

#[derive(Debug)]
pub struct ElectronConfigurationPart {
    pub energy_level: u8,
    pub orbital: Orbital,
    pub electrons: u8,
}

#[derive(Debug)]
pub enum YearDiscovered {
    Year(u16),
    Ancient,
}
