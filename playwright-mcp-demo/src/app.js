const state = {
  loggedIn: false,
  tasks: []
};

function $(sel) { return document.querySelector(sel); }
function el(tag, props = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(props).forEach(([k, v]) => {
    if (k === 'dataset') Object.entries(v).forEach(([dk, dv]) => node.dataset[dk] = dv);
    else if (k in node) node[k] = v; else node.setAttribute(k, v);
  });
  children.forEach(c => node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c));
  return node;
}

function renderTasks() {
  const list = $('#task-list');
  list.innerHTML = '';
  state.tasks.forEach((t, i) => {
    const item = el('li', { className: 'task-item' }, [
      el('input', { type: 'checkbox', checked: !!t.done, 'aria-label': `Complete ${t.text}` }),
      el('span', { className: 'task-text' }, [t.text]),
      el('button', { className: 'delete-btn' }, ['Delete'])
    ]);

    item.querySelector('input').addEventListener('change', (e) => {
      state.tasks[i].done = e.target.checked;
    });
    item.querySelector('.delete-btn').addEventListener('click', () => {
      state.tasks.splice(i, 1);
      renderTasks();
    });
    list.appendChild(item);
  });
}

function initLogin() {
  $('#login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const u = $('#username').value.trim();
    const p = $('#password').value;
    setTimeout(() => {
      if (u && p) {
        state.loggedIn = true;
        // Very simple demo role handling: admin if username+password both 'admin'
        const isAdmin = u.toLowerCase() === 'admin' && p === 'admin';
        const role = isAdmin ? 'admin' : 'user';
        try { localStorage.setItem('demo-role', role); } catch {}
        $('#login-status').textContent = isAdmin ? `Logged in as admin` : `Logged in as ${u}`;
        $('#login-status').dataset.testid = isAdmin ? 'admin-login' : 'login-success';
      } else {
        state.loggedIn = false;
        $('#login-status').textContent = 'Login failed';
        $('#login-status').dataset.testid = 'login-failed';
      }
    }, 150);
  });
}

function initTasks() {
  $('#add-task').addEventListener('click', () => {
    const text = $('#new-task').value.trim();
    if (!text) return;
    state.tasks.push({ text, done: false });
    $('#new-task').value = '';
    renderTasks();
  });

  $('#clear-completed').addEventListener('click', () => {
    state.tasks = state.tasks.filter(t => !t.done);
    renderTasks();
  });
}

function initModal() {
  const dialog = $('#demo-modal');
  $('#open-modal').addEventListener('click', () => dialog.showModal());
  $('#close-modal').addEventListener('click', () => dialog.close());
}

function init() {
  initLogin();
  initTasks();
  initModal();
}

document.addEventListener('DOMContentLoaded', init);
