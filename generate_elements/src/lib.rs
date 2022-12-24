extern crate proc_macro;

use proc_macro::TokenStream;

// use proc_macro2::{Ident, Span};
use quote::quote;

use serde_json::from_str;

mod stage_1;
use stage_1::make_elements_idiomatic;

const PUB_CHEM_RAW_DATA: &'static str = include_str!("pub_chem.json");

#[proc_macro]
pub fn generate_elements(_: TokenStream) -> TokenStream {
    let element_data = from_str(PUB_CHEM_RAW_DATA).unwrap();
    let idiomatic_element_data = make_elements_idiomatic(element_data);

    quote! {
        fn showcase() {
            println!("Not done yet.");
        }
    }.into()
}