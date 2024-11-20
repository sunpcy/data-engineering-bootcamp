with

fct as (

    select * from {{ ref('fct_movements') }}

)

, final as (

    select
        company_name
        , variation_status as number_of_late
        , count(1) as record_number
    from fct
    -- where variation_status = "LATE" AND DATE_DIFF(CURRENT_DATE, DATE(actual_timestamp_utc), DAY) < 3
    where variation_status = "LATE" AND date(actual_timestamp_utc) >= date_add(current_date(), interval -3 day)
    group by 1,2
    order by 3 desc
    limit 10

)

select * from final