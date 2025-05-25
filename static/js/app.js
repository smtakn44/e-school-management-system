// E-School Management System JavaScript

$(document).ready(function () {
    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();

    // Initialize popovers
    $('[data-bs-toggle="popover"]').popover();

    // Auto-hide alerts after 5 seconds
    $('.alert').delay(5000).slideUp(300);

    // Form validation
    $('form').on('submit', function (e) {
        var form = this;
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        $(form).addClass('was-validated');
    });

    // Grade input validation
    $('input[name="grade"]').on('input', function () {
        var value = parseFloat($(this).val());
        if (value < 0 || value > 100) {
            $(this).addClass('is-invalid');
            $(this).next('.invalid-feedback').remove();
            $(this).after('<div class="invalid-feedback">Grade must be between 0 and 100</div>');
        } else {
            $(this).removeClass('is-invalid');
            $(this).next('.invalid-feedback').remove();
        }
    });

    // Confirm delete actions
    $('.btn-danger[data-action="delete"]').on('click', function (e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });

    // Auto-refresh for real-time updates (optional)
    if ($('.auto-refresh').length > 0) {
        setInterval(function () {
            location.reload();
        }, 30000); // Refresh every 30 seconds
    }

    // Search functionality
    $('#searchInput').on('keyup', function () {
        var value = $(this).val().toLowerCase();
        $('table tbody tr').filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    // Grade color coding
    $('.grade-display').each(function () {
        var grade = parseFloat($(this).text());
        if (grade >= 90) {
            $(this).addClass('text-success');
        } else if (grade >= 80) {
            $(this).addClass('text-info');
        } else if (grade >= 70) {
            $(this).addClass('text-warning');
        } else if (grade >= 60) {
            $(this).addClass('text-secondary');
        } else {
            $(this).addClass('text-danger');
        }
    });

    // Loading states for buttons
    $('.btn-loading').on('click', function () {
        var btn = $(this);
        var originalText = btn.html();
        btn.html('<span class="loading"></span> Loading...');
        btn.prop('disabled', true);

        setTimeout(function () {
            btn.html(originalText);
            btn.prop('disabled', false);
        }, 2000);
    });

    // Modal form handling
    $('.modal form').on('submit', function () {
        var modal = $(this).closest('.modal');
        var submitBtn = modal.find('button[type="submit"]');
        submitBtn.html('<span class="loading"></span> Processing...');
        submitBtn.prop('disabled', true);
    });

    // Clear modal forms when closed
    $('.modal').on('hidden.bs.modal', function () {
        $(this).find('form')[0].reset();
        $(this).find('.is-invalid').removeClass('is-invalid');
        $(this).find('.invalid-feedback').remove();
    });

    // Animate statistics cards
    $('.stats-card').each(function (index) {
        $(this).delay(index * 100).animate({
            opacity: 1,
            transform: 'translateY(0)'
        }, 500);
    });

    // Grade statistics calculation
    if ($('.grade-stats').length > 0) {
        updateGradeStatistics();
    }

    // Print functionality
    $('.btn-print').on('click', function () {
        window.print();
    });

    // Export functionality (basic CSV export)
    $('.btn-export').on('click', function () {
        var table = $(this).data('table');
        exportTableToCSV(table);
    });
});

// Function to update grade statistics
function updateGradeStatistics() {
    var grades = [];
    $('.grade-value').each(function () {
        var grade = parseFloat($(this).text());
        if (!isNaN(grade)) {
            grades.push(grade);
        }
    });

    if (grades.length > 0) {
        var average = grades.reduce((a, b) => a + b, 0) / grades.length;
        var highest = Math.max(...grades);
        var lowest = Math.min(...grades);

        $('.avg-grade').text(average.toFixed(1));
        $('.highest-grade').text(highest);
        $('.lowest-grade').text(lowest);
    }
}

// Function to export table to CSV
function exportTableToCSV(tableId) {
    var csv = [];
    var rows = document.querySelectorAll(tableId + " tr");

    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");

        for (var j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }

        csv.push(row.join(","));
    }

    downloadCSV(csv.join("\n"), "export.csv");
}

// Function to download CSV
function downloadCSV(csv, filename) {
    var csvFile = new Blob([csv], { type: "text/csv" });
    var downloadLink = document.createElement("a");
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
}

// Real-time notifications (placeholder for future implementation)
function showNotification(message, type = 'info') {
    var alertClass = 'alert-' + type;
    var alert = $('<div class="alert ' + alertClass + ' alert-dismissible fade show" role="alert">' +
        message +
        '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
        '</div>');

    $('.container').prepend(alert);

    setTimeout(function () {
        alert.fadeOut();
    }, 5000);
}

// Form validation helpers
function validateEmail(email) {
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

function validateUsername(username) {
    return username.length >= 3 && /^[a-zA-Z0-9]+$/.test(username);
}

// Grade calculation helpers
function calculateGPA(grades) {
    if (grades.length === 0) return 0;

    var points = grades.map(grade => {
        if (grade >= 90) return 4.0;
        else if (grade >= 80) return 3.0;
        else if (grade >= 70) return 2.0;
        else if (grade >= 60) return 1.0;
        else return 0.0;
    });

    return points.reduce((a, b) => a + b, 0) / points.length;
}

function getLetterGrade(numericGrade) {
    if (numericGrade >= 90) return 'A';
    else if (numericGrade >= 80) return 'B';
    else if (numericGrade >= 70) return 'C';
    else if (numericGrade >= 60) return 'D';
    else return 'F';
}

// Theme toggle (for future dark mode implementation)
function toggleTheme() {
    $('body').toggleClass('dark-theme');
    localStorage.setItem('theme', $('body').hasClass('dark-theme') ? 'dark' : 'light');
}

// Load saved theme
$(document).ready(function () {
    var savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        $('body').addClass('dark-theme');
    }
});