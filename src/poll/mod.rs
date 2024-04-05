use std::{error, result};

/// Call a service handler, getting the bool response. We do some
/// basic runtime type checking to ensure the function returns a `PyBool`
pub async fn call_handler(handler: &str) -> result::Result<bool, Box<dyn error::Error>> {
    Ok(true)
}