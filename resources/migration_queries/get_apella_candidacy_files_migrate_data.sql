copy (
select
    c.id candidacy_serial,
    p.id position_serial,
    c.candidate_id candidate_user_id,
    fh.id file_id,
    fh.type as file_type,
    fb.storedfilepath file_path,
    fb.originalfilename original_name,
    case
        when fb.date is null then '1970-01-01'
        else fb.date
    end as updated_at
from
    position p,
    positioncandidacies pc,
    candidacy c,
    (   select
            id,
            candidacy_id,
            null candidate_id
        from
            candidacyfile
        union
        select
            id,
            null candidacy_id,
            candidate_id
        from
            candidatefile
    ) cf,
    fileheader fh,
    filebody fb
where
    pc.position_id = p.id
    and pc.id = c.candidacies_id
    and (cf.candidacy_id = c.id or cf.candidate_id = c.candidate_id)
    and cf.id = fh.id
    and fh.currentbody_id = fb.id
    and fh.deleted is false
    and p.id in
    (1580743, 1579871, 1551754, 1608651, 1601475, 1601581, 1601660, 1601764, 1601847, 1555596,
     1563659, 1561195, 1560254, 1561064, 1570004, 1570773, 1570414, 1571299, 1565946, 1565859,
     1561324, 1555755, 1541621, 1542092, 1541455, 1541561, 1541967, 1541896, 1541007, 1541695,
     1541079, 1541158, 1541279, 1542031, 1542289, 1542390, 1541348, 1535131, 1535277, 1535432,
     1535522, 1535585, 1535672, 1535732, 1535797, 1535939, 1536072, 1536198, 1536332, 1536437,
     1536554, 1536685, 1536796, 1536866, 1536934, 1537043, 1537088, 1565081, 1564991, 1565278,
     1565382, 1574345, 1574479, 1574613, 1574715, 1574858, 1574938, 1575020, 1575122, 1575236,
     1575345, 1575414, 1556814, 1556937, 1557061, 1557211, 1557310, 1557441, 1557524, 1557630,
     1557727, 1557849, 1557930, 1558012, 1558110, 1558178, 1558270, 1558528, 1547298, 1547407,
     1547495, 1547573, 1548345, 1533766, 1534719, 1534955, 1539789, 1540004, 1472683, 1474379,
     1480451, 1481439, 1552600, 1554545, 1552800, 1552967, 1553115, 1553279, 1553396, 1553463,
     1553570, 1553645, 1553716, 1554030, 1554119, 1558320, 1558532, 1558665, 1558789, 1558852,
     1558938, 1559018, 1559189, 1559345, 1559531, 1559743, 1559839, 1559984, 1610365, 1610750,
     1610891, 1611056, 1609354, 1621373, 1621522, 1623252, 1624192, 1623376, 1629612, 1629827,
     1605770, 1629749, 1672432, 1672077, 1672168, 1630764, 1672960, 1673211, 1673587, 1673757,
     1673849, 1673929, 1722098, 1722229, 1722363, 1722440, 1722561, 1722635, 1629988, 1629650,
     1638542, 1638730, 1590586, 1612942, 1575723, 1724132, 1724526, 1724906, 1775695, 1776003,
     1776412, 1776822, 1777143, 1777224, 1777775, 1767288, 1766789, 1767383, 1767467, 1767061,
     1657836, 1723608, 1723844, 1723970, 1724124, 1724401, 1724518, 1724730, 1725867, 1726122,
     1725127, 1725266, 1725425, 1725575, 1774023, 1774202, 1774388, 1774832, 1775042, 1775214,
     1775463, 1775683, 1775811, 1775993, 1776284, 1776663, 1777037, 1777421, 1777867, 1778101,
     1787589, 1787708, 1787847, 1788043, 1788344, 1788459, 1788564, 1788710, 1788823, 1788943,
     1789084, 1789202, 1817351, 1817726, 1817920, 1818098, 1818220, 1818394, 1760604, 1765586,
     1765811, 1765967, 1766176, 1766240, 1831588, 1831700, 1847950, 1758487, 1758717, 1758927,
     1759109, 1759274, 1759431, 1605130, 1605270, 1606201, 1606282, 1606510, 1608435, 1608500,
     1946604, 1946976, 1947470, 1947717, 1817367, 1817538, 1819564, 1609938, 1610075, 1873762,
     1874214, 1874404, 1874547, 1874638, 1649475, 1648091, 1648711, 1649808, 1649994, 1650174,
     1649586, 1650350, 1650450, 1650518, 1651087, 1650668, 1585654, 1590885, 1632918, 1633053,
     1962358, 1973576, 1974258, 1588082, 1668226, 1587714, 1588340, 1587499, 1588489, 1587305,
     1586972, 1586724, 1638546, 1640176, 1640833, 1640496, 1640623, 1668422, 1668626, 1668781,
     1668974, 1669144, 1669346, 1767732, 1552129, 1552161, 1968381, 1852404, 1980653, 1855265,
     1854935, 1642348, 1642167, 1641707, 1585969, 1585800, 1585643, 1585354, 1585209, 1700464,
     1700312, 1904682, 1905054, 1905470, 1905662, 1905863, 1906150, 1906441, 1906698, 1907186,
     1577102, 1589128, 1674540, 1674723, 1674963, 1675127, 1886371, 1885833, 1885550, 1830738,
     1830539, 1830415, 1830239, 1830151, 1830025, 1829905, 1420589, 1420538, 1420485, 1420421,
     1420398, 1572524, 1844184, 1844334, 1844533, 1982482, 1982666, 1982849, 1983039, 1983255,
     1983443, 1983652, 1591506, 1592191, 1572289, 1633058, 1617047, 1592532, 1633326, 1591079,
     1591656, 1591792, 1591558, 1609204, 1608998, 1609094, 1592640, 1592024, 1591948, 1943074,
     1592753, 1592938, 1593082, 1551331, 1551459, 1618185, 1617736, 1572373, 1757285, 1572089,
     1591420, 1592278, 1591336, 1592458, 1592377, 1623755, 1622595, 1621648, 1621831, 1621947,
     1622024, 1622118, 1622189, 1622269, 1622433, 1622346, 1633564, 1633475, 1847704, 1847583,
     1960273, 1847413, 1570962, 1570777, 1570229, 1570369, 1570557, 2001723, 2001982, 2002227,
     2002554, 2006145, 2006324, 2006908, 2007219, 2007451, 1755992, 1756140, 1575648, 1575963,
     1576099, 1576124, 1576352, 1576455, 1576459, 1576565, 1576697, 1577086, 1577092, 1577368,
     1577372, 1577588, 1577699, 1578006, 1578116, 1578162, 1578257, 1578416, 1578657, 1578694,
     1578839, 1579288, 1579554, 1579751, 1579867, 1580046, 1580195, 1580199, 1580302, 1580503,
     1580507, 1580692, 1580838, 1580952, 1581053, 1581257, 1581346, 1581472, 1581602, 1582035,
     1582159, 1582260, 1582384, 1582493, 1582614, 1582686, 1582815, 1582990, 1583113, 1583230,
     1583340, 1583467, 1583630, 1583756, 1585981, 1586226, 1613660, 1613903, 1614140, 1614144,
     1614433, 1615134, 1615174, 1615741, 1615954, 1616227, 1616519, 1616652, 1617037, 1617043,
     1617424, 1617746, 1618486, 1618612, 1618616, 1618785, 1618898, 1619391, 1619495, 1619601,
     1619715, 1619817, 1619886, 1619972, 1620114, 1661881, 1662209, 1662804, 1663096, 1663371,
     1663606, 1663844, 1664115, 1942855, 1943662, 1944012, 1944134, 1944573, 1945920, 1949723,
     1950498, 1950807, 1951359, 1646617, 1647225, 1648715, 1646863, 1646417, 1648359, 1646979,
     1648500, 1647904, 1647087, 1648081, 1650381, 1649296, 1650684, 1649494, 1649816, 1676189,
     1676082, 1676332, 1675963, 1676460, 1676541, 1886030, 1886545, 1887123, 1885519, 1886898,
     1887425, 1887816, 1885734, 2014506, 2014801, 2015121, 2015351, 2015552, 2015740, 2016058,
     2016221, 2016376, 2016559, 2016726, 2016947, 2017230, 2017531, 2017679, 2017947, 2018162,
     2018360, 2018483, 2018685, 2018855, 2019029, 2019250, 2019522, 2019755, 2019936, 2020147,
     2020372, 2020555, 2043317, 2043446)
) to '/tmp/OldApellaCandidacyFileMigrationData.csv' with csv header delimiter ',';
