// Clean file to contrast with bad.js
const answer = 42;

function greet(name) {
  if (typeof name !== 'string') return;
  console.log('Hello, ' + name + '!');
}

function sum(nums) {
  if (!Array.isArray(nums)) return 0;
  return nums.reduce((acc, n) => acc + n, 0);
}

greet('World');
console.log('Sum:', sum([1, 2, 3]));
