pub fn get_pub_chem_json() {
    const PUB_CHEM_RAW_DATA: &'static str = include_str!("pub_chem.json");
    serde_json::from_str(PUB_CHEM_RAW_DATA).unwrap()
}