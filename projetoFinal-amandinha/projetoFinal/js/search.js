document.addEventListener('DOMContentLoaded', function() {
    const searchIcon = document.querySelector('.search-icon');
    const searchInput = document.getElementById('searchInput');
  
    function performSearch() {
      const searchTerm = searchInput.value.trim().toLowerCase();
  
      if (searchTerm === 'cafe' || searchTerm === 'café') {
        window.location.href = '/cafe2';
      } else if (searchTerm === 'bebida gourmet') {
        window.location.href = '/cafe1';
      } else if (searchTerm === 'cafeteiras') {
        window.location.href = '/cafe3';
      } else if (searchTerm === 'capsulas' || searchTerm === 'cápsulas') {
        window.location.href = '/cafe4';
      } else {
        alert('Nenhuma correspondência encontrada.');
      }
    }
  
    searchIcon.addEventListener('click', performSearch);
  
    searchInput.addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
        performSearch();
      }
    });
  });
  