with

fct as (

    select * from {{ ref('fct_movements') }}

)

, final as (

    select
        train_id
        , count(variation_status) as number_of_off_route
    from fct
    where variation_status = "OFF ROUTE"
    group by train_id
    order by number_of_off_route desc
    limit 1

)

select * from final