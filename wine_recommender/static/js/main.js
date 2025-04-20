// Initialize tooltips
document.addEventListener("DOMContentLoaded", function () {
	// Initialize all tooltips
	var tooltipTriggerList = [].slice.call(
		document.querySelectorAll('[data-bs-toggle="tooltip"]')
	);
	var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
		return new bootstrap.Tooltip(tooltipTriggerEl);
	});

	// Initialize all popovers
	var popoverTriggerList = [].slice.call(
		document.querySelectorAll('[data-bs-toggle="popover"]')
	);
	var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
		return new bootstrap.Popover(popoverTriggerEl);
	});

	// Handle trait selection limit
	const traitCheckboxes = document.querySelectorAll(".trait-checkbox");
	if (traitCheckboxes.length > 0) {
		traitCheckboxes.forEach((checkbox) => {
			checkbox.addEventListener("change", function () {
				const maxSelect = parseInt(this.dataset.maxSelect);
				const checkedTraits = document.querySelectorAll(
					".trait-checkbox:checked"
				);

				if (checkedTraits.length > maxSelect) {
					this.checked = false;
					Swal.fire({
						title: "Selection Limit Reached",
						text: `You can only select up to ${maxSelect} traits.`,
						icon: "warning",
						confirmButtonText: "OK",
					});
				}

				// Disable remaining checkboxes if limit is reached
				if (checkedTraits.length >= maxSelect) {
					traitCheckboxes.forEach((cb) => {
						if (!cb.checked) {
							cb.disabled = true;
						}
					});
				} else {
					traitCheckboxes.forEach((cb) => {
						cb.disabled = false;
					});
				}
			});
		});
	}

	// Handle newsletter form submission
	const newsletterForm = document.querySelector(".footer-newsletter");
	if (newsletterForm) {
		newsletterForm.addEventListener("submit", function (e) {
			e.preventDefault();
			const email = this.querySelector('input[type="email"]').value;

			// Show success message using SweetAlert2
			Swal.fire({
				title: "Thank you!",
				text: "You have successfully subscribed to our newsletter.",
				icon: "success",
				confirmButtonText: "OK",
			}).then((result) => {
				if (result.isConfirmed) {
					this.reset();
				}
			});
		});
	}

	// Handle mobile menu
	const navbarToggler = document.querySelector(".navbar-toggler");
	const navbarCollapse = document.querySelector(".navbar-collapse");

	if (navbarToggler && navbarCollapse) {
		navbarToggler.addEventListener("click", function () {
			navbarCollapse.classList.toggle("show");
		});

		// Close mobile menu when clicking outside
		document.addEventListener("click", function (e) {
			if (
				!navbarCollapse.contains(e.target) &&
				!navbarToggler.contains(e.target)
			) {
				navbarCollapse.classList.remove("show");
			}
		});
	}

	// Smooth scroll for anchor links
	document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
		anchor.addEventListener("click", function (e) {
			const href = this.getAttribute("href");
			if (href === "#") return;

			e.preventDefault();
			const target = document.querySelector(href);
			if (target) {
				target.scrollIntoView({
					behavior: "smooth",
					block: "start",
				});
			}
		});
	});

	// Add animation to cards on scroll
	const cards = document.querySelectorAll(".card");
	const observer = new IntersectionObserver(
		(entries) => {
			entries.forEach((entry) => {
				if (entry.isIntersecting) {
					entry.target.classList.add("animate__animated", "animate__fadeInUp");
				}
			});
		},
		{
			threshold: 0.1,
		}
	);

	cards.forEach((card) => {
		observer.observe(card);
	});
});

// Auto-hide alerts after 5 seconds
window.setTimeout(function () {
	$(".alert")
		.fadeTo(500, 0)
		.slideUp(500, function () {
			$(this).remove();
		});
}, 5000);

// Confirm dangerous actions
document.querySelectorAll("[data-confirm]").forEach(function (element) {
	element.addEventListener("click", function (e) {
		if (!confirm(this.dataset.confirm)) {
			e.preventDefault();
		}
	});
});

// Handle form validation
function validateForm(formId) {
	const form = document.getElementById(formId);
	if (!form) return true;

	let isValid = true;
	const requiredFields = form.querySelectorAll("[required]");

	requiredFields.forEach((field) => {
		if (!field.value.trim()) {
			isValid = false;
			field.classList.add("is-invalid");
		} else {
			field.classList.remove("is-invalid");
		}
	});

	return isValid;
}

// Handle file upload preview
function handleFileUpload(input, previewId) {
	const preview = document.getElementById(previewId);
	if (!input || !preview) return;

	input.addEventListener("change", function () {
		const file = this.files[0];
		if (file) {
			const reader = new FileReader();
			reader.onload = function (e) {
				preview.src = e.target.result;
			};
			reader.readAsDataURL(file);
		}
	});
}

// Handle dynamic form fields
function addFormField(containerId, templateId) {
	const container = document.getElementById(containerId);
	const template = document.getElementById(templateId);
	if (!container || !template) return;

	const newField = template.content.cloneNode(true);
	container.appendChild(newField);
}

// Handle dynamic form field removal
function removeFormField(button) {
	const field = button.closest(".form-field");
	if (field) {
		field.remove();
	}
}

// Export functions for use in other files
window.validateForm = validateForm;
window.handleFileUpload = handleFileUpload;
window.addFormField = addFormField;
window.removeFormField = removeFormField;

// Common utility functions
function showAlert(title, text, icon) {
	Swal.fire({
		title: title,
		text: text,
		icon: icon,
		confirmButtonColor: "#722f37",
	});
}

// Form validation helpers
function validateEmail(email) {
	const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	return re.test(email);
}

function validatePassword(password) {
	return {
		length: password.length >= 8,
		number: /\d/.test(password),
		uppercase: /[A-Z]/.test(password),
		special: /[!@#$%^&*]/.test(password),
	};
}

// Handle flash messages
document.addEventListener("DOMContentLoaded", function () {
	const flashMessages = document.querySelectorAll(".alert");
	flashMessages.forEach((message) => {
		setTimeout(() => {
			message.classList.remove("show");
			setTimeout(() => message.remove(), 150);
		}, 5000);
	});
});
