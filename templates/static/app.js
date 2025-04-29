async function loadTrending() {
  const res = await fetch('/trending');
  const videos = await res.json();
  renderVideos(videos);
}

async function search() {
  const query = document.getElementById('searchInput').value;
  if (!query) return;
  const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
  const videos = await res.json();
  renderVideos(videos);
}

async function loadChannel(channelId) {
  const res = await fetch(`/channel?c=${encodeURIComponent(channelId)}`);
  const data = await res.json();
  if (data.latestVideos) {
    renderVideos(data.latestVideos);
  } else {
    alert('チャンネルが見つかりませんでした');
  }
}

async function loadPlaylist(playlistId) {
  const res = await fetch(`/playlist?p=${encodeURIComponent(playlistId)}`);
  const data = await res.json();
  if (data.videos) {
    renderVideos(data.videos);
  } else {
    alert('プレイリストが見つかりませんでした');
  }
}

function renderVideos(videos) {
  const content = document.getElementById('content-area');
  content.innerHTML = '';
  videos.forEach(video => {
    const div = document.createElement('div');
    div.className = 'video-item';
    if (video.videoId) {
      div.innerHTML = `
        <a href="/watch?v=${video.videoId}">
          <img src="${video.thumbnail || ''}" alt="サムネイル">
        </a>
        <p>${video.title || video.author}</p>
      `;
    } else if (video.title) {
      div.innerHTML = `<p>🔍 ${video.title}</p>`;
    }
    content.appendChild(div);
  });
}

function showChannelInput() {
  const channelId = prompt('チャンネルIDを入力してください');
  if (channelId) loadChannel(channelId);
}

function showPlaylistInput() {
  const playlistId = prompt('プレイリストIDを入力してください');
  if (playlistId) loadPlaylist(playlistId);
}
