$(document).ready(function () {
    var successMessage = $("#jq-notification");
    var isProcessing = false;

    // Плавное появление корзины
    setTimeout(function() {
        $('.cart-fixed-wrapper').css('opacity', '1');
    }, 500);

    // Общая функция для обновления UI с анимациями
    function updateCartUI(data) {
        // Анимация изменения счетчика
        $("#goods-in-cart-count")
            .fadeOut(100, function() {
                $(this).text(data.total_quantity).fadeIn(200);
            });
        
        // Анимация обновления содержимого корзины
        $("#cart-items-container")
            .css("opacity", 0.7)
            .html(data.cart_items_html)
            .animate({ opacity: 1 }, 300);
        
        // Стильное уведомление
        successMessage
            .hide()
            .html(`<i class="bi bi-check-circle-fill me-2"></i>${data.message}`)
            .css({
                'position': 'fixed',
                'top': '20px',
                'left': '50%',
                'transform': 'translateX(-50%)',
                'z-index': '1060',
                'padding': '15px 25px',
                'border-radius': '8px',
                'background-color': '#28a745',
                'color': 'white',
                'box-shadow': '0 4px 15px rgba(0,0,0,0.2)'
            })
            .fadeIn(400)
            .delay(2500)
            .fadeOut(400);
    }

    // Обработчик добавления в корзину с анимацией кнопки
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();
        if (isProcessing) return;
        isProcessing = true;

        var button = $(this);
        
        // Анимация нажатия
        button.css('transform', 'scale(0.95)');
        // Показываем индикатор загрузки
        // button.html('<span class="spinner-border spinner-border-sm me-2" role="status"></span>Добавляем...');

        $.ajax({
            type: "POST",
            url: button.attr("href"),
            data: {
                product_id: button.data("product-id"),
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function(data) {
                updateCartUI(data);
                
                // // Анимация успешного добавления
                // button.html('<i class="bi bi-check2 me-2"></i>Добавлено')
                //       .css('background-color', '#28a745')
                //       .animate({ transform: 'scale(1.1)' }, 200)
                //       .delay(1000)
                //       .animate({ 
                //           transform: 'scale(1)',
                //           backgroundColor: '#212529'
                //       }, 300, function() {
                //           button.html(originalHtml);
                //       });
            },
            error: function() {
                // Анимация ошибки
                button.html('<i class="bi bi-x-circle-fill me-2"></i>Ошибка')
                      .css('background-color', '#dc3545')
                      .animate({ transform: 'scale(1.1)' }, 200)
                      .delay(1000)
                      .animate({ 
                          transform: 'scale(1)',
                          backgroundColor: '#212529'
                      }, 300, function() {
                          button.html(originalHtml);
                      });
            },
            complete: function() {
                isProcessing = false;
                
            }
        });
    });

    // Обработчик удаления из корзины с анимацией
    $(document).on("click", ".cart-btn-remove", function (e) {
        e.preventDefault();
        if (isProcessing) return;
        isProcessing = true;

        var button = $(this);
        var cartItem = button.closest('.cart-item');
        
        // Анимация нажатия
        button.css('transform', 'scale(0.9)');
        
        $.ajax({
            type: "POST",
            url: button.attr("href"),
            data: {
                cart_id: button.data("cart-id"),
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(), // Альтернативный способ
            },
            success: function(data) {
                // Проверка успешного удаления
                if (data.success) {
                    // Анимация удаления с fadeOut и slideUp
                    cartItem.animate(
                        { 
                            opacity: 0,
                            height: 0,
                            paddingTop: 0,
                            paddingBottom: 0,
                            marginBottom: 0
                        }, 
                        800,
                        function() {
                            $(this).remove();
                            updateCartUI(data);

                            if (data.total_quantity === 0) {
                                location.reload();
                            }
                        }
                    );
                } else {
                    console.error("Ошибка удаления:", data.message);
                    updateCartUI(data);
                }
            },
            error: function(xhr) {
                console.error("AJAX ошибка:", xhr.responseText);
                button.animate({ transform: 'scale(1)' }, 200);
            },
            complete: function() {
                isProcessing = false;
            }
        });
    });

    // Общая функция для изменения количества с анимацией
    function handleQuantityChange(e, change) {
        e.preventDefault();
        if (isProcessing) return;
        isProcessing = true;

        var button = $(this);
        var $input = button.closest('.quantity-control').find('.quantity-input');
        var newValue = parseInt($input.val()) + change;

        if ((change > 0 && newValue > 50) || (change < 0 && newValue < 1)) {
            isProcessing = false;
            return;
        }

        // Анимация изменения количества
        $input.animate({ opacity: 0.5 }, 100)
              .val(newValue)
              .animate({ opacity: 1 }, 100);
        
        $.ajax({
            type: "POST",
            url: button.data("cart-change-url"),
            data: {
                cart_id: button.data("cart-id"),
                quantity: newValue,
                csrfmiddlewaretoken: button.find("[name=csrfmiddlewaretoken]").val(),
            },
            success: function(data) {
                // Анимация кнопки
                button.css('color', '#d4af37')
                      .animate({ transform: 'scale(1.2)' }, 100)
                      .animate({ transform: 'scale(1)' }, 100, function() {
                          $(this).css('color', '');
                      });
                updateCartUI(data);
            },
            error: function() {
                console.log("Ошибка при изменении количества");
            },
            complete: function() {
                isProcessing = false;
            }
        });
    }

    $(document).on("click", ".cart-btn-decrement", function(e) {
        handleQuantityChange.call(this, e, -1);
    });

    $(document).on("click", ".cart-btn-increment", function(e) {
        handleQuantityChange.call(this, e, 1);
    });

    // Анимация при открытии корзины
    $('#modalButton').on('click', function() {
        $('#cartModal').on('shown.bs.modal', function() {
            $('#cart-items-container .cart-item').each(function(i) {
                $(this).css({
                    'opacity': 0,
                    'transform': 'translateX(20px)'
                }).delay(100*i).animate({
                    'opacity': 1,
                    'transform': 'translateX(0)'
                }, 300);
            });
        });
    });

    // Форматирование телефона
    document.getElementById('id_phone_number')?.addEventListener('input', function(e) {
        var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    });

    // Валидация формы с анимацией
    $('#create_order_form')?.on('submit', function(event) {
        var phoneNumber = $('#id_phone_number').val();
        if (!/^\(\d{3}\) \d{3}-\d{4}$/.test(phoneNumber)) {
            $('#phone_number_error')
                .hide()
                .css({ opacity: 0, height: 0 })
                .show()
                .animate({ opacity: 1, height: 'auto' }, 300);
            event.preventDefault();
        } else {
            $('#phone_number_error').fadeOut(200);
            $('#id_phone_number').val(phoneNumber.replace(/[()\-\s]/g, ''));
        }
    });


    // Адаптивное позиционирование корзины
    function updateCartPosition() {
        const cartWrapper = $('.cart-fixed-wrapper');
        if ($(window).width() <= 768) {
            cartWrapper.css({
                'right': '15px',
                'bottom': '15px',
                'top': 'auto'
            });
        } else {
            cartWrapper.css({
                'right': '30px',
                'top': '100px',
                'bottom': 'auto'
            });
        }
    }

    updateCartPosition();
    $(window).resize(updateCartPosition);
});

// $(document).ready(function() {
//     // Адаптивное позиционирование корзины
//     function updateCartPosition() {
//         const cartWrapper = $('.cart-fixed-wrapper');
//         if ($(window).width() <= 768) {
//             // Для мобильных - в правом нижнем углу
//             cartWrapper.css({
//                 'right': '15px',
//                 'bottom': '15px',
//                 'top': 'auto'
//             });
//         } else {
//             // Для ПК - в правом верхнем углу
//             cartWrapper.css({
//                 'right': '30px',
//                 'top': '80px',
//                 'bottom': 'auto'
//             });
//         }
//     }

//     // Инициализация и обработка ресайза
//     updateCartPosition();
//     $(window).resize(updateCartPosition);

//     // Плавное появление корзины
//     setTimeout(function() {
//         $('.cart-fixed-wrapper').css('opacity', '1');
//     }, 300);
    
//     // Анимация при добавлении в корзину
//     $(document).on('ajaxSuccess', function() {
//         $('#goods-in-cart-count')
//             .css('transform', 'scale(1.5)')
//             .animate({ transform: 'scale(1)' }, 300);
//     });
// });