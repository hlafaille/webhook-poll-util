use std::process::exit;
use pyo3::{types::{PyAnyMethods, PyDict, PyString}, Python};
use tokio::fs;
use tracing::info;
mod config;
mod poll;
mod webhook;
mod util;
mod handler;

/// Main program loop
///
/// # Returns
/// An `i32`, our exit status code.
async fn poll_loop() -> i32 {
    info!("loading python context");
    pyo3::prepare_freethreaded_python();
    Python::with_gil(|py| {
        let module = py.import_bound("handlers.jellyfin").unwrap();
        let url = module.getattr("URL").unwrap();
        let entrypoint = module.getattr("entrypoint").unwrap();

        let fake_api_response = PyString::new_bound(py, r#"{"message": "api is here"}"#);

        let entrypoint_response = entrypoint.call1((fake_api_response,)).unwrap();
        println!("{}", entrypoint_response);
    });

    // loop {
    //     let response_content = util::net::send_request("https://google.com").await.expect("Failed to poll");
    //     println!("{}", response_content);
    //     break;
    // }
    return 0;
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    info!("webhook poll utility :)");
    info!("starting poll loop");

    exit(poll_loop().await);
}
