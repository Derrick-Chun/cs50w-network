// ---- CSRF helper ----
function getCookie(name) {
    const m = document.cookie.match(new RegExp('(^|; )' + name + '=([^;]+)'));
    return m ? decodeURIComponent(m[2]) : null;
  }
  const CSRF = getCookie('csrftoken');
  
  // Find the closest .post card
  function findPost(el) {
    return el.closest('.post');
  }
  
  // Swap a post's content <p> for a textarea
  function startEditing(card) {
    const contentEl = card.querySelector('[data-role="content"]');
    if (!contentEl) return;
  
    // Avoid duplicating editors
    if (card.dataset.editing === '1') return;
    card.dataset.editing = '1';
  
    const original = contentEl.textContent.trim();
  
    const ta = document.createElement('textarea');
    ta.className = 'form-control';
    ta.rows = 3;
    ta.value = original;
  
    // Buttons
    const saveBtn = document.createElement('button');
    saveBtn.className = 'btn btn-sm btn-primary mt-2';
    saveBtn.textContent = 'Save';
  
    const cancelBtn = document.createElement('button');
    cancelBtn.className = 'btn btn-sm btn-light mt-2 ml-2';
    cancelBtn.textContent = 'Cancel';
  
    // Replace content with editor
    contentEl.replaceWith(ta);
    // Button row
    const btnRow = document.createElement('div');
    btnRow.className = 'mt-2';
    btnRow.appendChild(saveBtn);
    btnRow.appendChild(cancelBtn);
    ta.insertAdjacentElement('afterend', btnRow);
  
    // Save
    saveBtn.addEventListener('click', async () => {
      const url = card.dataset.editUrl;
      const newContent = ta.value.trim();
      if (!newContent) return;
  
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': CSRF,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ content: newContent })
      });
  
      if (!res.ok) {
        alert('Failed to save changes.');
        return;
      }
  
      const data = await res.json();
      const p = document.createElement('p');
      p.className = 'mb-0';
      p.setAttribute('data-role', 'content');
      p.textContent = data.content;
  
      btnRow.remove();
      ta.replaceWith(p);
      delete card.dataset.editing;
    });
  
    // Cancel
    cancelBtn.addEventListener('click', () => {
      const p = document.createElement('p');
      p.className = 'mb-0';
      p.setAttribute('data-role', 'content');
      p.textContent = original;
  
      btnRow.remove();
      ta.replaceWith(p);
      delete card.dataset.editing;
    });
  }
  
  // Toggle like/unlike
  async function toggleLike(card, button) {
    const url = card.dataset.likeUrl;
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF,
        'Accept': 'application/json'
      }
    });
  
    if (!res.ok) {
      alert('Failed to toggle like.');
      return;
    }
    const data = await res.json();
    const likesEl = card.querySelector('[data-role="likes"]');
    if (likesEl) likesEl.textContent = `❤️ ${data.likes_count}`;
    button.textContent = data.liked ? 'Unlike' : 'Like';
  }
  
  // Event delegation
  document.addEventListener('click', (e) => {
    const t = e.target;
  
    // Edit
    if (t.matches('[data-action="edit"]')) {
      e.preventDefault();
      const card = findPost(t);
      if (card) startEditing(card);
    }
  
    // Like
    if (t.matches('[data-action="like"]')) {
      e.preventDefault();
      const card = findPost(t);
      if (card) toggleLike(card, t);
    }
  });
  