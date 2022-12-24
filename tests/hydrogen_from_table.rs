use periodic_table_rs::{Element, PERIODIC_TABLE};

#[test]
fn main() {
    const HYDROGEN: &Element = PERIODIC_TABLE[0];

    println!("{:?}", HYDROGEN.atomic_mass);
    println!("{:?}", HYDROGEN.boiling_point);
    println!("{:?}", HYDROGEN.density);
}