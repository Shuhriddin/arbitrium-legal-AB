document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. Eased Slow Smooth Scroll
    // ==========================================
    // Disable JS-driven smooth scroll; use immediate scroll to target
    function slowSmoothScrollTo(targetSelector) {
        const target = document.querySelector(targetSelector);
        if (!target) return;
        const navbar = document.getElementById('navbar');
        const navbarHeight = navbar ? navbar.offsetHeight : 80;
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
        window.scrollTo({ top: targetPosition, behavior: 'smooth' });
    }

    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            e.preventDefault();
            
            const navMenu = document.getElementById('nav-menu');
            const mobileToggle = document.getElementById('mobile-toggle');
            if (navMenu && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                if (mobileToggle) {
                    mobileToggle.classList.remove('active');
                    mobileToggle.querySelector('i').className = 'fa-solid fa-bars';
                }
            }
            
            slowSmoothScrollTo(targetId, 700);
        });
    });

    // ==========================================
    // 2. Header Scroll Effect
    // ==========================================
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ==========================================
    // 3. Mobile Menu Toggle Button
    // ==========================================
    const mobileToggle = document.getElementById('mobile-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            mobileToggle.classList.toggle('active');
            const icon = mobileToggle.querySelector('i');
            if (navMenu.classList.contains('active')) {
                icon.className = 'fa-solid fa-xmark';
            } else {
                icon.className = 'fa-solid fa-bars';
            }
        });
    }

    // ==========================================
    // 4. Modal Toggles & Controls
    // ==========================================
    const modalOverlay = document.getElementById('modal-overlay');
    const modalClose = document.getElementById('modal-close');
    const openModalBtns = document.querySelectorAll('.open-modal-btn');
    const modalCategorySelect = document.getElementById('modal-category');

    function openModal(category) {
        if (modalOverlay) {
            if (category && modalCategorySelect) {
                modalCategorySelect.value = category;
            } else if (modalCategorySelect) {
                modalCategorySelect.selectedIndex = 0;
            }
            
            const modalForm = modalOverlay.querySelector('.application-form');
            if (modalForm) modalForm.reset();
            
            document.getElementById('modal-success-msg').classList.add('hidden');
            document.getElementById('modal-error-msg').classList.add('hidden');
            if (modalForm) modalForm.classList.remove('hidden');
            
            modalOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeModal() {
        if (modalOverlay) {
            modalOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    openModalBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            openModal(category);
        });
    });

    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }

    if (modalOverlay) {
        modalOverlay.addEventListener('click', function(e) {
            if (e.target === modalOverlay) {
                closeModal();
            }
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (modalOverlay && modalOverlay.classList.contains('active')) {
                closeModal();
            }
            const bModal = document.getElementById('blog-modal');
            if (bModal && bModal.classList.contains('active')) {
                bModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        }
    });

    // ==========================================
    // 5. Phone Number Mask & Enforcer
    // ==========================================
    const phoneInputs = document.querySelectorAll('.phone-mask');
    
    phoneInputs.forEach(input => {
        if (!input.value.startsWith('+998')) {
            input.value = '+998';
        }
        
        input.addEventListener('input', function(e) {
            let value = this.value;
            
            if (!value.startsWith('+998')) {
                if (value.length < 4) {
                    this.value = '+998';
                } else {
                    this.value = '+998' + value.replace(/\D/g, '');
                }
            }
            
            const prefix = '+998';
            let suffix = this.value.substring(4);
            suffix = suffix.replace(/\D/g, '');
            
            if (suffix.length > 9) {
                suffix = suffix.substring(0, 9);
            }
            
            this.value = prefix + suffix;
        });

        input.addEventListener('click', function() {
            if (this.selectionStart < 4) {
                this.setSelectionRange(4, 4);
            }
        });
        
        input.addEventListener('keydown', function(e) {
            if (this.selectionStart < 4 && (e.key === 'Backspace' || e.key === 'ArrowLeft')) {
                e.preventDefault();
            }
        });
    });

    // ==========================================
    // 6. FAQ Accordion Collapsible Logic
    // ==========================================
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(q => {
        q.addEventListener('click', function() {
            const item = this.parentElement;
            const answer = this.nextElementSibling;
            
            const isActive = item.classList.contains('active');
            
            // Close all FAQ items for single accordion open state
            document.querySelectorAll('.faq-item').forEach(el => {
                el.classList.remove('active');
                el.querySelector('.faq-answer').style.maxHeight = null;
            });
            
            // If the clicked item was not active, open it
            if (!isActive) {
                item.classList.add('active');
                // Calculate actual height dynamically
                answer.style.maxHeight = answer.scrollHeight + 'px';
            }
        });
    });

    // ==========================================
    // 7. Dynamic Frontend Localization (No Reload)
    // ==========================================
    const translationsDataElement = document.getElementById('translations-data');
    let translations = {};
    if (translationsDataElement) {
        try {
            translations = JSON.parse(translationsDataElement.textContent);
        } catch(e) {
            console.error("Failed to parse translations JSON:", e);
        }
    }

    function applyTranslations(lang) {
        if (!translations[lang]) return;
        const dict = translations[lang];

        // 1. Text elements
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (dict[key]) {
                if (el.tagName === 'SELECT') {
                    const options = el.options;
                    for (let i = 0; i < options.length; i++) {
                        const optKey = options[i].getAttribute('data-i18n');
                        if (optKey && dict[optKey]) {
                            options[i].text = dict[optKey];
                        }
                    }
                } else {
                    const icon = el.querySelector('i');
                    if (icon) {
                        const textSpan = el.querySelector('span[data-i18n]') || el;
                        if (textSpan !== el) {
                            textSpan.innerText = dict[key];
                        } else {
                            const iconHTML = icon.outerHTML;
                            el.innerHTML = dict[key] + ' ' + iconHTML;
                        }
                    } else {
                        if (key === 'hero_title' || key === 'hero_subtitle') {
                            el.innerHTML = dict[key];
                        } else {
                            el.innerText = dict[key];
                        }
                    }
                }
            }
        });

        // 2. Input and Textarea placeholders
        const inputs = document.querySelectorAll('[data-i18n-placeholder]');
        inputs.forEach(input => {
            const key = input.getAttribute('data-i18n-placeholder');
            if (dict[key]) {
                input.placeholder = dict[key];
            }
        });

        // 3. Document configurations
        document.documentElement.setAttribute('lang', lang);

        if (dict['meta_title']) {
            document.title = dict['meta_title'];
        }
        const metaDesc = document.getElementById('meta-desc');
        if (metaDesc && dict['meta_desc']) {
            metaDesc.setAttribute('content', dict['meta_desc']);
        }
        
        // Update globe dropdown active states
        const langCurrentLabel = document.getElementById('lang-current-label');
        if (langCurrentLabel) langCurrentLabel.textContent = lang.toUpperCase();
        document.querySelectorAll('.lang-option').forEach(opt => {
            if (opt.getAttribute('data-lang') === lang) {
                opt.classList.add('active');
            } else {
                opt.classList.remove('active');
            }
        });


        // Update dynamic database content with language variants
        const langTexts = document.querySelectorAll('.lang-text');
        langTexts.forEach(el => {
            const text = el.getAttribute('data-text-' + lang);
            if (text) {
                el.textContent = text;
            }
        });

        localStorage.setItem('preferred_language', lang);

        // Notify session in background
        fetch(`/set-language/?lang=${lang}`)
            .catch(err => console.log("Silent lang update error:", err));
            
        // If an FAQ item is currently expanded, recalculate its scrollHeight
        const openFaqAnswer = document.querySelector('.faq-item.active .faq-answer');
        if (openFaqAnswer) {
            openFaqAnswer.style.maxHeight = openFaqAnswer.scrollHeight + 'px';
        }
    }

    // Globe icon dropdown toggle
    const langSwitcher = document.getElementById('lang-switcher');
    const langToggleBtn = document.getElementById('lang-toggle-btn');
    const langDropdown = document.getElementById('lang-dropdown');

    if (langToggleBtn && langSwitcher) {
        langToggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            langSwitcher.classList.toggle('open');
        });
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (langSwitcher && !langSwitcher.contains(e.target)) {
            langSwitcher.classList.remove('open');
        }
    });

    const langOptions = document.querySelectorAll('.lang-option');
    langOptions.forEach(opt => {
        opt.addEventListener('click', function(e) {
            e.preventDefault();
            const selectedLang = this.getAttribute('data-lang');
            applyTranslations(selectedLang);
            if (langSwitcher) langSwitcher.classList.remove('open');
        });
    });

    const storedLang = localStorage.getItem('preferred_language');
    if (storedLang && (storedLang === 'uz' || storedLang === 'ru')) {
        const currentDocLang = document.documentElement.lang;
        if (storedLang !== currentDocLang) {
            applyTranslations(storedLang);
        }
    }

    // ==========================================
    // 8. AJAX Form Submission
    // ==========================================
    const forms = document.querySelectorAll('.application-form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!this.checkValidity()) {
                this.reportValidity();
                return;
            }

            const actionUrl = this.getAttribute('action');
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            
            submitBtn.disabled = true;
            
            const activeLang = document.documentElement.lang || 'uz';
            const sendingText = activeLang === 'ru' ? 'Отправка...' : 'Yuborilmoqda...';
            submitBtn.innerText = sendingText;

            const parentCard = this.closest('.form-card') || this.closest('.modal-box');
            const successMsg = parentCard.querySelector('.success-msg');
            const errorMsg = parentCard.querySelector('.error-msg');

            if (successMsg) successMsg.classList.add('hidden');
            if (errorMsg) errorMsg.classList.add('hidden');

            const formData = new FormData(this);
            const dataObject = {};
            formData.forEach((value, key) => {
                dataObject[key] = value;
            });

            const csrfTokenInput = this.querySelector('[name=csrfmiddlewaretoken]');
            const csrfToken = csrfTokenInput ? csrfTokenInput.value : '';

            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(dataObject)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Server error');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    form.reset();
                    const phoneInput = form.querySelector('.phone-mask');
                    if (phoneInput) phoneInput.value = '+998';

                    if (successMsg) {
                        successMsg.classList.remove('hidden');
                    }
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                    
                    form.classList.add('hidden');
                    
                    if (parentCard.classList.contains('modal-box')) {
                        setTimeout(() => {
                            closeModal();
                        }, 3000);
                    }
                } else {
                    if (errorMsg) errorMsg.classList.remove('hidden');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                }
            })
            .catch(error => {
                console.error('Submission error:', error);
                if (errorMsg) errorMsg.classList.remove('hidden');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            });
        });
    });

    // ==========================================
    // 9. Blog Article Modal Handler
    // ==========================================
    const blogModal = document.getElementById('blog-modal');
    const blogModalClose = document.getElementById('blog-modal-close');
    const blogReadBtns = document.querySelectorAll('.blog-read-btn');
    
    function openBlogModal(btn) {
        if (!blogModal) return;
        
        const currentLang = document.documentElement.lang || 'uz';
        
        // Get values from button attributes depending on current language
        const title = btn.getAttribute('data-title-' + currentLang) || btn.getAttribute('data-title') || '';
        const content = btn.getAttribute('data-content-' + currentLang) || btn.getAttribute('data-content') || '';
        const lawCode = btn.getAttribute('data-law-code-' + currentLang) || btn.getAttribute('data-law-code') || '';
        const lawArticle = btn.getAttribute('data-law-article-' + currentLang) || btn.getAttribute('data-law-article') || '';
        
        const modalTitle = document.getElementById('blog-modal-title');
        const modalContent = document.getElementById('blog-modal-content');
        const modalLaw = document.getElementById('blog-modal-law');
        
        if (modalTitle) modalTitle.textContent = title;
        if (modalContent) modalContent.innerHTML = content;
        
        if (modalLaw) {
            let lawText = '';
            if (lawCode && lawArticle) {
                lawText = `${lawCode}, ${lawArticle}`;
            } else if (lawCode) {
                lawText = lawCode;
            } else if (lawArticle) {
                lawText = lawArticle;
            }
            modalLaw.textContent = lawText;
            if (lawText) {
                modalLaw.style.display = 'block';
            } else {
                modalLaw.style.display = 'none';
            }
        }
        
        blogModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    function closeBlogModal() {
        if (blogModal) {
            blogModal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
    
    blogReadBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            openBlogModal(this);
        });
    });
    
    if (blogModalClose) {
        blogModalClose.addEventListener('click', closeBlogModal);
    }
    
    if (blogModal) {
        blogModal.addEventListener('click', function(e) {
            if (e.target === blogModal) {
                closeBlogModal();
            }
        });
    }

});
