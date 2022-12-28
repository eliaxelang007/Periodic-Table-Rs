use serde::de::value::MapDeserializer;
use serde::Deserialize;

use serde_json::Value;

use serde_with::{serde_as, DisplayFromStr};

use heck::ToSnakeCase;

use std::iter::zip;
use std::collections::HashMap;

pub fn get_pub_chem_elements(unidiomatic: RawDataFormat) -> Vec<PubChemElement> {
    let table = unidiomatic.Table;
    let element_keys = table.Columns.Column.iter().map(|key| key.to_snake_case());

    let rows = table.Row;

    let mut idiomatic = Vec::<PubChemElement>::with_capacity({
        let element_count = rows.len();
        assert_eq!(element_count, 118);
        element_count
    });

    for element_values in rows.iter().map(|row| &row.Cell) {
        let idiomatic_element_json = zip(
            element_keys.clone(), 
            element_values.clone().map(|property| Value::from(property))
        ).collect::<HashMap<String, Value>>();

        let idiomatic_element = PubChemElement::deserialize(
            MapDeserializer::new(idiomatic_element_json.into_iter())
        ).unwrap();

        idiomatic.push(idiomatic_element);
    }

    idiomatic
}

#[derive(Deserialize)]
pub struct PubChemElement {
    #[serde_as(as = "DisplayFromStr")]
    pub atomic_number: u8,
    pub symbol: String,
    pub name: String,
    #[serde_as(as = "DisplayFromStr")]
    pub atomic_mass: f64,
    #[serde(deserialize_with = "deserialize_color")]
    pub cpk_hex_color: Option<Color>,
    #[serde(deserialize_with = "deserialize_electron_configuration")]
    pub electron_configuration: Vec<ElectronConfigurationPart>,
    #[serde_as(as = "DisplayFromStr")]
    pub electronegativity: Option<f64>,
    #[serde_as(as = "DisplayFromStr")]
    pub atomic_radius: Option<u16>,
    #[serde_as(as = "DisplayFromStr")]
    pub ionization_energy: Option<f64>,
    #[serde_as(as = "DisplayFromStr")]
    pub electron_affinity: Option<f64>,
    #[serde_as(as = "DisplayFromStr")]
    pub oxidation_states: Option<Vec<i8>>,
    pub standard_state: String,
    #[serde_as(as = "DisplayFromStr")]
    pub melting_point: Option<f64>,
    #[serde_as(as = "DisplayFromStr")]
    pub boiling_point: Option<f64>,
    #[serde_as(as = "DisplayFromStr")]
    pub density: Option<f64>,
    pub group_block: String,
    pub year_discovered: String,
}

#[derive(Deserialize)]
#[allow(non_snake_case)]
pub struct RawDataFormat {  Table: TableFormat }

#[derive(Deserialize)]
#[allow(non_snake_case)]
struct TableFormat {  Columns: ColumnsFormat,  Row: Vec<RowFormat> }

#[derive(Deserialize)]
#[allow(non_snake_case)]
struct RowFormat { Cell: [String; 17] }

#[derive(Deserialize)]
#[allow(non_snake_case)]
struct ColumnsFormat {  Column: [String; 17] }