SELECT 
    tchp_providers.npi,
    gender,
    providerName,
    firstName,
    middleName,
    lastName,
    degree,
    location_number,
    locationName,
    providerOrgName,
    locationPrimary,
    addressLine1,
    addressLine2,
    city,
    state,
    zip,
    county,
    lat,
    lon,
    specialtyGroup,
    specialtyDesc,
    location_count,
    IF(location_count = 1, 'N', 'Y') multi_location,
    IF(ISNULL(nppes_match),
        'N',
        nppes_match) nppes_match,
    nppes_flat.Provider_Last_Name_legal_name,
    provider_other_last_name,
    provider_first_name,
    provider_middle_name,
    provider_name_prefix_text,
    Provider_Other_Credential_Text,
    Provider_First_Line_Business_Mailing_Address,
    Provider_Second_Line_Business_Mailing_Address,
    Provider_Business_Mailing_Address_City_Name,
    Provider_Business_Mailing_Address_State_Name,
    Provider_Business_Mailing_Address_Postal_Code,
    Provider_First_Line_Business_Practice_Location_Address,
    Provider_Second_Line_Business_Practice_Location_Address,
    Provider_Business_Practice_Location_Address_City_Name,
    Provider_Business_Practice_Location_Address_State_Name,
    Provider_Business_Practice_Location_Address_Postal_Code,
    last_update_date,
    provider_gender_code,
    is_sole_proprietor
FROM
    tchp_providers
        INNER JOIN
    tchp_locations ON tchp_locations.npi = tchp_providers.npi
        INNER JOIN
    tchp_specialties ON tchp_specialties.npi = tchp_providers.npi
        INNER JOIN
    nppes_flat ON nppes_flat.npi = tchp_providers.npi
        LEFT OUTER JOIN
    (SELECT 
        npi, location_count
    FROM
        (SELECT 
        npi, COUNT(*) location_count
    FROM
        tchp_locations
    GROUP BY npi) location_totals) multi_location_providers ON multi_location_providers.npi = tchp_providers.npi
        LEFT OUTER JOIN
    (SELECT DISTINCT
        tchp_locations.npi, 'Y' nppes_match
    FROM
        tchp_locations
    INNER JOIN nppes_flat ON nppes_flat.npi = tchp_locations.npi
    WHERE
        (CONCAT(UPPER(LEFT(addressLine1, 8)), LEFT(zip, 5)) = CONCAT(LEFT(Provider_First_Line_Business_Mailing_Address, 8), LEFT(Provider_Business_Mailing_Address_Postal_Code, 5))
            OR CONCAT(UPPER(LEFT(addressLine1, 8)), LEFT(zip, 5)) = CONCAT(LEFT(Provider_First_Line_Business_Practice_Location_Address, 8), LEFT(Provider_Business_Practice_Location_Address_Postal_Code, 5)))) nppes_matches ON nppes_matches.npi = tchp_providers.npi