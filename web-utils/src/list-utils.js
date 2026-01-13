// List utilities for client-side rendering
const foo = 1;
const bar = 2;

export function areEqual(a, b) {
  if (a === b) {
    console.log('Equal!\n');
  }
}

export function renderList(items) {
  const localBar = 'local';
  console.log(localBar);

  const arr = [1, 2, 3];
  arr.push(4);

  for (let i = 0; i < items.length; i++) {
    console.log(items[i]);
  }

  areEqual(foo, bar);
}
