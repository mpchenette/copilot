// List utilities for client-side rendering (with intentional issues for lint demo)
var foo = 1 // missing semicolon, uses var
let bar = 2
let unused = 3

export function areEqual(a, b) {
  if (a == b) { // eqeqeq violation
    console.log("Equal!\n"); // double quotes
  }
}

export function renderList(items) {
  let bar = 'shadowed';
  console.log(bar)

  // undefined variable usage
  console.log(result)

  // prefer-const violation
  let arr = [1,2,3]
  arr.push(4)

  // mixed spaces and tabs			
  for (var i = 0; i < items.length; i++) {
    console.log(items[i])
  }

  areEqual(foo, bar)
}
