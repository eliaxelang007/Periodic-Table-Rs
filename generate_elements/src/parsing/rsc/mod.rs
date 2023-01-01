use super::ELEMENT_COUNT;
use scraper::{Html, Selector};

pub fn get_rsc_json() {
    use tokio::runtime::Runtime;

    let runtime = Runtime::new().unwrap();

    runtime.block_on(async {
        use tokio::spawn;

        let client = Client::new();

        for atomic_number in 1..=ELEMENT_COUNT {
            spawn(
                async {
                    get_element_data(atomic_number, client).await.unwrap()
                }
            );
        }
    })
}

use reqwest::Client;

async fn get_element_data(atomic_number: u8, client: Client) -> Vec {
    let response = client.get(
        format!("https://www.rsc.org/periodic-table/element/{atomic_number}/", atomic_number = atomic_number)
    )
    .send()
    .await.unwrap()
    .text()
    .await.unwrap();

    let html = Html::parse_document(response.as_str());

    let property_table_selector = Selector::parse("table[class=element_hover_table_ca] > tbody").unwrap();
    let property_table = html.select(&property_table_selector).next().unwrap();

    let row_selector = Selector::parse("tr").unwrap();

    property_table.select(&row_selector).map(
        |row| {
            let cell_selector = Selector::parse("td").unwrap();

            row.select(&cell_selector).map(|cell| {
                cell.text().collect::<String>()
            })
        }
    ).collect::<Vec<_>>()
}