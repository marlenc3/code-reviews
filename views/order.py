import socket


def process_request_view(request):
    """
    example request
    {
    order_total: 123.99,
    request_id: '9ae543c6-9efb-4d8a-ab9b-5fcfb04a137b',
    source: 'shopify'
    datetime: '2021-09-17T14:32:16.953535'
    }
    """

    order_total = request['order_total']
    source = request['source']
    order_time = request['datetime']

    order, created = Order.objects.get_or_create(source=source, order_total=order_total)

    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    hostname = socket.gethostname()
    logger.debug("Created new order from %s from %s at %s on machine %s from %s", source, order_time, requestid, ip,
                 hostname)

    if created:
        emit_event(
            body={'type': 'OrderCreated', 'source': source},
            to='shipping_service'
        )
        emit_event(
            body={'type': 'OrderCreated', 'source': source},
            to='billing_service'
        )
        emit_event(
            body={'type': 'OrderCreated', 'source': source},
            to='ERP_integration_service'
        )

        return 200
    else:
        return 500