const API = (path, params) => {
  const url = new URL(`http://127.0.0.1:8000${path}`);
  if (params) Object.entries(params).forEach(([k,v]) => (v!=='' && v!=null) && url.searchParams.append(k, v));
  return fetch(url).then(r => r.json());
};

let state = { page: 1 };

function stars(r) {
  if (r == null) return '—';
  const full = Math.round(r * 2) / 2; // round to 0.5
  return '★'.repeat(Math.floor(full)) + (full%1? '½' : '') + ' ' + r.toFixed(1);
}

function fmtTime(t) { return t == null ? '—' : `${t} min`; }

function rowHTML(r) {
  return `<tr class="border-t hover:bg-gray-50 cursor-pointer" data-id="${r.id}">
    <td class="py-2 px-3">${r.title}</td>
    <td class="py-2 px-3">${r.cuisine ?? '—'}</td>
    <td class="py-2 px-3">${fmtTime(r.total_time)}</td>
    <td class="py-2 px-3">${stars(r.rating)}</td>
    <td class="py-2 px-3">${r.serves ?? '—'}</td>
  </tr>`;
}

function nutrientsTable(r) {
  const fields = [
    ['Calories (kcal)','calories_kcal'],
    ['Carbs (g)','carbohydrate_g'],
    ['Protein (g)','protein_g'],
    ['Fat (g)','fat_g'],
    ['Sat. fat (g)','saturated_fat_g'],
    ['Sugar (g)','sugar_g'],
    ['Fiber (g)','fiber_g'],
    ['Sodium (mg)','sodium_mg'],
    ['Cholesterol (mg)','cholesterol_mg'],
  ];
  const rows = fields.map(([label, key]) => `<tr><td class="py-1 pr-4 text-gray-600">${label}</td><td class="py-1">${r[key] ?? '—'}</td></tr>`).join('');
  return `<table class="text-sm">${rows}</table>`;
}

async function load(page=1) {
  state.page = page;
  const params = {
    page,
    limit: document.getElementById('limit').value,
    sort: document.getElementById('sort').value,
  };

  const title = document.getElementById('fTitle').value.trim();
  const cuisine = document.getElementById('fCuisine').value.trim();
  const total_time_max = document.getElementById('fTime').value;
  const calories_max = document.getElementById('fCalories').value;
  const rating_min = document.getElementById('fRatingMin').value;

  let resp;
  if (title || cuisine || total_time_max || calories_max || rating_min) {
    resp = await API('/api/recipes/search', { ...params, title, cuisine, total_time_max, calories_max, rating_min });
  } else {
    resp = await API('/api/recipes', params);
  }

  const tbody = document.getElementById('tbody');
  tbody.innerHTML = '';
  if (resp.data.length === 0) {
    document.getElementById('empty').classList.remove('hidden');
  } else {
    document.getElementById('empty').classList.add('hidden');
    tbody.innerHTML = resp.data.map(rowHTML).join('');
    tbody.querySelectorAll('tr').forEach(tr => tr.addEventListener('click', () => openDrawer(resp.data.find(r => r.id == tr.dataset.id))));
  }

  document.getElementById('count').textContent = `Total: ${resp.total}`;
  const pages = Math.max(1, Math.ceil(resp.total / params.limit));
  document.getElementById('pageInfo').textContent = `Page ${resp.page} of ${pages}`;
  document.getElementById('prev').disabled = resp.page <= 1;
  document.getElementById('next').disabled = resp.page >= pages;
}

function openDrawer(r) {
  const d = document.getElementById('details');
  d.innerHTML = `
    <h2 class="text-2xl font-semibold mb-2">${r.title}</h2>
    <p class="text-gray-600 mb-2">${r.description ?? ''}</p>
    <div class="grid grid-cols-2 gap-4 mb-4">
      <div><div class="text-xs uppercase text-gray-500">Cuisine</div>${r.cuisine ?? '—'}</div>
      <div><div class="text-xs uppercase text-gray-500">Serves</div>${r.serves ?? '—'}</div>
      <div><div class="text-xs uppercase text-gray-500">Prep</div>${r.prep_time ?? '—'} min</div>
      <div><div class="text-xs uppercase text-gray-500">Cook</div>${r.cook_time ?? '—'} min</div>
      <div><div class="text-xs uppercase text-gray-500">Total</div>${r.total_time ?? '—'} min</div>
      <div><div class="text-xs uppercase text-gray-500">Rating</div>${stars(r.rating)}</div>
    </div>
    <h3 class="font-semibold mt-4 mb-1">Nutrients</h3>
    ${nutrientsTable(r)}
    <h3 class="font-semibold mt-4 mb-1">Ingredients</h3>
    <ul class="list-disc ml-6 text-sm">${JSON.parse(r.ingredients || "[]").map(i => `<li>${i}</li>`).join("")}</ul>
    <h3 class="font-semibold mt-4 mb-1">Instructions</h3>
    <ol class="list-decimal ml-6 text-sm">${JSON.parse(r.instructions || "[]").map(i => `<li class="mb-1">${i}</li>`).join("")}</ol>
    ${r.url ? `<a href="${r.url}" target="_blank" class="inline-block mt-3 text-blue-600 underline">Original Source</a>` : ''}
  `;
  const drawer = document.getElementById('drawer');
  drawer.classList.remove('hidden');
  drawer.classList.add('flex');
}

document.getElementById('closeDrawer').addEventListener('click', () => {
  const drawer = document.getElementById('drawer');
  drawer.classList.add('hidden');
  drawer.classList.remove('flex');
});

document.getElementById('btnSearch').addEventListener('click', () => load(1));
document.getElementById('limit').addEventListener('change', () => load(1));
document.getElementById('sort').addEventListener('change', () => load(1));
document.getElementById('prev').addEventListener('click', () => load(Math.max(1, (state.page||1) - 1)));
document.getElementById('next').addEventListener('click', () => load((state.page||1) + 1));

load(1);
