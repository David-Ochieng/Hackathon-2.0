// Mobile menu toggle
const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');

mobileMenuButton.addEventListener('click', () => {
  mobileMenu.classList.toggle('hidden');
});

// Modal functionality
const newEntryBtn = document.getElementById('newEntryBtn');
const entryModal = document.getElementById('entryModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelEntryBtn = document.getElementById('cancelEntryBtn');

newEntryBtn.addEventListener('click', () => {
  entryModal.classList.remove('hidden');
});

closeModalBtn.addEventListener('click', () => {
  entryModal.classList.add('hidden');
});

cancelEntryBtn.addEventListener('click', () => {
  entryModal.classList.add('hidden');
});

entryModal.addEventListener('click', (e) => {
  if (e.target === entryModal) {
    entryModal.classList.add('hidden');
  }
});

// Mood Chart
const ctx = document.getElementById('moodChart').getContext('2d');
const moodChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    datasets: [{
      label: 'Mood Score',
      data: [3, 4, 3, 5, 4, 5, 4],
      backgroundColor: 'rgba(124, 58, 237, 0.1)',
      borderColor: 'rgba(124, 58, 237, 1)',
      borderWidth: 2,
      tension: 0.4,
      fill: true,
      pointBackgroundColor: 'rgba(124, 58, 237, 1)',
      pointRadius: 5,
      pointHoverRadius: 7
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: function(context) {
            const moods = ['', 'Excited', 'Happy', 'Neutral', 'Sad', 'Angry'];
            return moods[context.raw] || context.raw;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        min: 1,
        max: 5,
        ticks: {
          callback: function(value) {
            const moods = ['', '😊', '🙂', '😐', '🙁', '😠'];
            return moods[value] || value;
          }
        }
      }
    }
  }
});

// Form submissions
document.getElementById('quickMoodForm').addEventListener('submit', function(e) {
  e.preventDefault();
  alert('Quick mood entry saved!');
  this.reset();
});

document.getElementById('journalForm').addEventListener('submit', function(e) {
  e.preventDefault();
  alert('Journal entry saved successfully!');
  this.reset();
  entryModal.classList.add('hidden');
});
