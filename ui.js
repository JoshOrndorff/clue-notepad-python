"use strict"

document.addEventListener("DOMContentLoaded", function(){

  // Add the player boxes and their event listeners dynamically
  var characters = ["Prof. Plum", "Col. Mustard", "Mrs. Peacock", "Miss Scarlet", "Mrs. White", "Mr. Green"]
  var table = document.getElementById("players")
  var template = document.getElementById("template")

  for (var charHolder of characters){
    // Grab the elements
    let newRow = template.cloneNode(true)
    let nameBox = newRow.getElementsByClassName("pname")[0]
    let meButton = newRow.getElementsByClassName("me")[0]

    // Update the attributes
    newRow.removeAttribute("id")
    nameBox.placeholder = charHolder

    // DOM and event listeners
    table.appendChild(newRow)
    nameBox.addEventListener("input", () => {
      meButton.disabled = nameBox.value === ""
      meButton.checked = false
    })
  }

  // Remove the template from the dom
  template.remove()

  // Event listener for the continue button
  document.getElementById("continue").addEventListener("click", () => {
    // TODO
  })


})
