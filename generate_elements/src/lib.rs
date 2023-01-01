extern crate proc_macro;

use proc_macro::TokenStream;

mod parsing;
use parsing::pub_chem::get_pub_chem_json;
use parsing::rsc::get_rsc_json;

#[proc_macro]
pub fn generate_elements(_: TokenStream) -> TokenStream {    
    let pub_chem_json = get_pub_chem_json();
    let rsc_json = get_rsc_json();

    /*
    use serde_json::from_str;

    const PUB_CHEM_RAW_DATA: &'static str = include_str!("pub_chem.json");

    let pub_chem_json = from_str(PUB_CHEM_RAW_DATA).unwrap();

    use pub_chem::idiomize_elements;
    let idiomatic_element_json = idiomize_elements(pub_chem_json);

    use pub_chem::fill_in_element_properties;
    let revised_element_json = fill_in_element_properties(idiomized_elements);


    let cleaned_elements_json = clean_elements(revised_elements);


    let element_structures = structure_elements(cleaned_elements);
    
    generate_tokens(element_structures);
    */
}