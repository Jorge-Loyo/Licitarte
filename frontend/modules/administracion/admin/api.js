export const api = {
  async get(url) {
    const response = await fetch(url);
    return await response.json();
  },

  async post(url, data) {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await response.json();
  },

  async put(url, data) {
    const response = await fetch(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await response.json();
  },

  async delete(url) {
    const response = await fetch(url, { method: 'DELETE' });
    return await response.json();
  },

  async uploadFile(url, file) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(url, {
      method: 'POST',
      body: formData
    });
    return await response.json();
  }
};
