use std::{error, result};

/// Send a GET request, getting the response
pub async fn send_request(url: &str) -> result::Result<String, Box<dyn error::Error>> {
    let bytes = reqwest::get(url).await?.bytes().await?;
    Ok(String::from_utf8(bytes.to_vec())?)
}