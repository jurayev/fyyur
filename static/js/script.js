window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

function deleteVenue(e) {
  const id = e.currentTarget.dataset.id;
  fetch(`/venues/${id}/delete`, { method: 'DELETE' })
    .then(response => {
      if (response.ok) {
        console.log("SUCCESS:", response);
        window.location.href = "/";
      } else {
        console.log("ERROR:", response);
      }
    })
};

function deleteArtist(e) {
  const id = e.currentTarget.dataset.id;
  fetch(`/artists/${id}/delete`, { method: 'DELETE' })
    .then(response => {
      if (response.ok) {
        console.log("SUCCESS:", response);
        window.location.href = "/";
      } else {
        console.log("ERROR:", response);
      }
    })
};
