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
	document.querySelectorAll('.alert').forEach(alert => {
		alert.style.transition = 'opacity 0.5s';
		alert.style.opacity = '0';
		setTimeout(() => {
			alert.style.height = '0';
			alert.style.margin = '0';
			alert.style.padding = '0';
			setTimeout(() => alert.remove(), 500);
		}, 500);
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

// Signup form step validation
async function validateSignupStep(step) {
	const form = document.getElementById('signupForm');
	const formData = new FormData(form);
	const stepData = {};
	
	// Get data for current step
	const currentStep = document.querySelector(`.form-step[data-step="${step}"]`);
	const inputs = currentStep.querySelectorAll('input, select, textarea');
	inputs.forEach(input => {
		if (input.type === 'checkbox' || input.type === 'radio') {
			if (input.checked) {
				if (input.name.endsWith('[]')) {
					const name = input.name.slice(0, -2);
					if (!stepData[name]) stepData[name] = [];
					stepData[name].push(input.value);
				} else {
					stepData[input.name] = input.value;
				}
			}
		} else {
			stepData[input.name] = input.value;
		}
	});

	try {
		// Get CSRF token from meta tag or hidden input
		const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || 
						 document.querySelector('input[name="csrf_token"]')?.value;
						 
		if (!csrfToken) {
			console.error('CSRF token not found');
			return false;
		}

		const response = await fetch('/auth/signup/validate-step', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken
			},
			credentials: 'same-origin',
			body: JSON.stringify({
				step: step,
				data: stepData
			})
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const result = await response.json();
		
		// Clear existing errors
		currentStep.querySelectorAll('.validation-error').forEach(el => el.remove());
		currentStep.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
		
		if (!result.valid) {
			// Show errors
			Object.entries(result.errors).forEach(([field, message]) => {
				const input = currentStep.querySelector(`[name="${field}"]`);
				if (input) {
					input.classList.add('is-invalid');
					const errorDiv = document.createElement('div');
					errorDiv.className = 'validation-error invalid-feedback';
					errorDiv.textContent = message;
					input.parentNode.appendChild(errorDiv);
				}
			});
			return false;
		}
		
		return true;
	} catch (error) {
		console.error('Error validating step:', error);
		return false;
	}
}
