-- delete HOQM data values
delete from datavalue dv where dv.dataelementid in 
(
 select dataelementid from dataelement where name like 'HOQM%'
);

-- delete HOQM data value audit
delete from datavalueaudit dva where dva.dataelementid in 
(
 select dataelementid from dataelement where name like 'HOQM%'
);

-- get data valua audits for organisation id
select *
from datavalueaudit da
join organisationunit ou
 on da.organisationunitid=ou.organisationunitid
where ou.uid='iPjpfPR1Ptd';

-- delete all data value audits for organisation id
delete
from datavalueaudit da
using organisationunit ou
 where da.organisationunitid=ou.organisationunitid
 and ou.uid='iPjpfPR1Ptd';