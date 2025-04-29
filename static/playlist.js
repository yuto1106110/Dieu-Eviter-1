window.onload = async () => {
  const res = await fetch(`/playlist?p=${encodeURIComponent(playlistId)}`);
  const data = await res.json();
  const content = document.getElementById('content-area');

  if (data.videos) {
    data.videos.forEach(video => {
      const div = document.createElement('div');
      div.className = 'video-item';
      div.innerHTML = `
        <a href="/watch?v=${video.videoId}">
          <img src="${video.videoThumbnails ? video.videoThumbnails[0].url : ''}" width="320">
        </a>
        <p>${video.title}</p>
      `;
      content.appendChild(div);
    });
  }
};
