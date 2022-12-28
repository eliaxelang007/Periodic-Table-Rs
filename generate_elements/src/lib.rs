extern crate proc_macro;

use serde_json::from_str;

mod stage_1;
use stage_1::get_pub_chem_elements;

mod stage_2;
use stage_2::fill_in_missing;

mod stage_3;
use stage_3::generate_rust_types;

const PUB_CHEM_RAW_DATA: &'static str = include_str!("pub_chem.json");

#[proc_macro]
pub fn generate_elements(_: TokenStream) -> TokenStream {
    let element_data = from_str(PUB_CHEM_RAW_DATA).unwrap();

    let idiomatic_element_data = get_pub_chem_elements(element_data);
    let filled_in = fill_in_missing(idiomatic_element_data);

    generate_rust_types()
}