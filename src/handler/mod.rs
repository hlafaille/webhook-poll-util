use std::{error, path, result};

use pyo3::Python;

pub struct HandlerBuilder<'a> {
    // `SERVICE_URL` declared in the Python file
    service_url: Option<String>,
    // `WEBHOOK_URL` declared in the Python file
    webhook_url: Option<String>,
    // `INTERVAL` declared in the Python file
    interval: Option<i64>,
    // The path to the Python file
    path: Option<path::PathBuf>,
    // A reference to the Python GIL
    gil: Option<&'a Python<'static>>
}

impl HandlerBuilder {
    /// Create an empty `HandlerBuilder`.
    ///
    /// # Returns
    /// A new, emtpy `HandlerBuilder`.
    pub fn new() -> Self {
        HandlerBuilder {
            service_url: None,
            webhook_url: None,
            interval: None,
            path: None,
            gil: todo!(),
        }
    }
    
    pub fn gil(mut self, gil: &Python<'static>) -> Self {
        
        self
    }

    /// Populate from a Python file.
    ///
    /// # Arguments
    /// * `gil`: Reference to an active Python GIL.
    /// * `py_content`: Contents of the Python file.
    ///
    /// # Returns
    /// `Self`
    pub fn from_py(self, gil: &Python<'static>, py_content: &str) -> Self {
        // 
    }

    /// Create a new `Handler`.
    pub fn build() -> result::Result<Handler, Box<dyn error::Error>> {
        todo!()
    }
}

/// A `Handler`. Handlers tell us:
/// * Which resource needs polling
/// * How to handle the poll response
/// * How long we should wait between polls
/// * Which webhook gets called when the event occurrs
/// * Optionally, how to format the request payload going to the webhook
///
/// `Handler`'s are described in Python and required to have a `SERVICE_URL`, `WEBHOOK_URL`, and `INTERVAL` constant declared
/// at the top level. At minimum, we also require a `handle_response()` synchronous function that acepts a `str`. Arg #0 is
/// known as the `response` from calling `GET` on your `SERVICE_URL`. It contains the HTTP content.
pub struct Handler {
    // `SERVICE_URL` declared in the Python file
    service_url: String,
    // `WEBHOOK_URL` declared in the Python file
    webhook_url: String,
    // `INTERVAL` declared in the Python file
    interval: Option<i64>,
}

// todo: since we can only havce one interpreter in this process with pyo3, we need to figure out how to share that
