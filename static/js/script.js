/* script.js
Small helpers:
		- mobile menu toggle
		- accordion toggles
		- mock prediction calculation and update UI
		- accessible focus/aria updates
		*/

		document.addEventListener('DOMContentLoaded', () => {
				// --- mobile menu toggle ---
				const mobileToggle = document.getElementById('mobile-menu-toggle');
				const mobileMenu = document.getElementById('mobile-menu');

				if (mobileToggle && mobileMenu) {
						mobileToggle.addEventListener('click', () => {
								const expanded = mobileToggle.getAttribute('aria-expanded') === 'true';
								mobileToggle.setAttribute('aria-expanded', String(!expanded));
								const hidden = mobileMenu.getAttribute('aria-hidden') === 'true';
								mobileMenu.setAttribute('aria-hidden', String(!hidden));
								mobileMenu.style.display = hidden ? 'block' : 'none';
						});
				}

				// --- accordion ---
				document.querySelectorAll('.acc-item').forEach(button => {
						button.addEventListener('click', () => {
								const expanded = button.getAttribute('aria-expanded') === 'true';
								button.setAttribute('aria-expanded', String(!expanded));

								// toggle panel next element
								const panel = button.nextElementSibling;
								if (!panel) return;
								panel.style.display = expanded ? 'none' : 'block';
								// also adjust the chevron (simple character swap)
								const chev = button.querySelector('.chev');
								if (chev) chev.textContent = expanded ? '▸' : '▾';
						});

						// initially collapse panels that are aria-expanded=false
						const panel = button.nextElementSibling;
						if (panel && button.getAttribute('aria-expanded') !== 'true') panel.style.display = 'none';
				});

				// --- mock prediction ---
				const form = document.getElementById('predict-form');
				const resultNumber = document.querySelector('.value-number');
				const resultText = document.getElementById('result-text');

				async function predict(gdp, co2, mortality) {
						const response = await fetch("/predict", {
								method: "POST",
								headers: { "Content-type": "application/json"},
								body: JSON.stringify({gdp, co2, mortality})
						});

						const data = await response.json();
						return data.prediction;
				}

				if (form) {
						form.addEventListener('submit', async (evt) => {
								evt.preventDefault();
								const gdp = form.querySelector('#gdp').value;
								const co2 = form.querySelector('#co2').value;
								const mortality = form.querySelector('#mortality').value;

								// basic validation
								if (!gdp || !co2 || !mortality) {
										resultText.textContent = 'Please complete all fields.';
										return;
								}

								const prediction = await predict(gdp, co2, mortality);
								resultNumber.textContent = prediction.toFixed(1);

								// Qualitative feedback based on life expectancy
								let feedback = "";
								if (prediction < 60) {
										feedback = "Poor — below global averages.";
								} else if (prediction >= 60 && prediction < 70) {
										feedback = "Fair — slightly below average.";
								} else if (prediction >= 70 && prediction < 75) {
										feedback = "Good — around global average.";
								} else if (prediction >= 75 && prediction < 80) {
										feedback = "Very Good — above average.";
								} else {
										feedback = "Excellent — top life expectancy!";
								}

								resultText.textContent = `This projection suggests a life expectancy of ${prediction.toFixed(1)} years. ${feedback}`;
								resultNumber.parentElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
						});
				}
				// --- small hover animation for chart bars (pure UI) ---
				document.querySelectorAll('.chart-svg .bar').forEach(bar => {
						bar.addEventListener('mouseenter', () => bar.style.transform = 'scaleY(1.03)');
						bar.addEventListener('mouseleave', () => bar.style.transform = 'scaleY(1)');
				});


				// set initial mobile menu display none for a11y
				if (mobileMenu) {
						mobileMenu.setAttribute('aria-hidden', 'true');
						mobileMenu.style.display = 'none';
				}
		});
