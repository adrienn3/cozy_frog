import { Application } from "@hotwired/stimulus"
import { FetchRequest } from '@rails/request.js'

const application = Application.start()

// Configure Stimulus development experience
application.debug = false
window.Stimulus   = application

// document.addEventListener("DOMContentLoaded", function() {
//     const button = document.querySelector("#pull-button");

//     button.addEventListener("click", async function(event) {
//       event.preventDefault();

//       const url = "/pull_item";
//       const data = {
//         pull: true
//       };

//         const request = new FetchRequest('POST', url, {
//             body: JSON.stringify(data)
//           })
//           const response = await request.perform()
//           if (response.ok) {
//             const body = await response.text
//           }
//     });
//   });

export { application }
