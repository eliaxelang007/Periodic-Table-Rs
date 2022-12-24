use serde::{Deserialize};
use heck::ToSnakeCase;

pub fn make_elements_idiomatic(unidiomatic: RawDataFormat) -> Vec<IdiomaticElement> {
    let table = unidiomatic.Table;
    let key_names = table.Columns.Column.iter().map(|key| key.to_snake_case());

    let rows = table.Row;

    let idiomatic = Vec::<IdiomaticElement>::with_capacity({
        let element_count = rows.len();
        assert_eq!(element_count, 118);
        element_count
    });

    for row in rows.iter().map(|row| row.Cell) {
        
    }

    idiomatic
}

pub struct IdiomaticElement {
    atomic_number: String,
    symbol: String,
    name: String,
    atomic_mass: String,
    cpk_hex_color: String,
    electron_configuration: String,
    electronegativity: String,
    atomic_radius: String,
    ionization_energy: String,
    electron_affinity: String,
    oxidation_states: String,
    standard_state: String,
    melting_point: String,
    density: String,
    group_block: String,
    year_discovered: String
}

#[derive(Deserialize)]
pub struct RawDataFormat { #[allow(non_snake_case)] Table: TableFormat }

#[derive(Deserialize)]
struct TableFormat { #[allow(non_snake_case)] Columns: ColumnsFormat, #[allow(non_snake_case)] Row: Vec<RowFormat> }

#[derive(Deserialize)]
struct RowFormat { #[allow(non_snake_case)] Cell: [String; 17] }

#[derive(Deserialize)]
struct ColumnsFormat { #[allow(non_snake_case)] Column: Vec<String> }