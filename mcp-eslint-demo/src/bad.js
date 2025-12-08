// Intentionally includes common lint issues for demo
var foo = 1 // missing semicolon, uses var
let bar = 2
let unused = 3

function compare(a, b) {
  if (a == b) { // eqeqeq violation
    console.log("Equal!\n"); // double quotes
  }
}

function shadow() {
  let bar = 'shadowed';
  console.log(bar)
}

// undefined variable usage
console.log(result)

// prefer-const violation
let arr = [1,2,3]
arr.push(4)

// mixed spaces and tabs			
for (var i = 0; i < arr.length; i++) {
  console.log(arr[i])
}

compare(foo, bar)
shadow()
