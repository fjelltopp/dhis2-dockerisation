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

