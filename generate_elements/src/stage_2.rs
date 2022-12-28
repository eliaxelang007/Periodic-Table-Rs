use tokio::runtime::Runtime;

use super::stage_1::PubChemElement;

pub fn fill_in_missing(elements: Vec<PubChemElement>) -> representation {
    let element = Runtime::new().unwrap().block_on(get_rsc_elements()); 
}

async fn get_rsc_elements() -> Vec