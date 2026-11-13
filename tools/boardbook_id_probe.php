<?php
// Probe BoardBook document IDs for PPS (org 915) with HEAD requests and print "id,status" in ID order.
// 200 = a document with that ID is viewable under org 915; a missing (or other-org) document answers 302 to "/".
// Usage: php tools/boardbook_id_probe.php [start=14695005] [count=10000] [concurrency=10]
// Supplied by the repository owner 2026-11-13; run hourly by a scheduled task.

const BASE_URL = 'https://meetings.boardbook.org/Documents/WebViewer/915?file=';

function makeHandle(int $id): CurlHandle
{
    $ch = curl_init(BASE_URL . $id);
    curl_setopt_array($ch, [
        CURLOPT_NOBODY         => true,   // HEAD request, headers only
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_FOLLOWLOCATION => false,  // a missing document redirects to /, so keep the 302
        CURLOPT_TIMEOUT        => 15,
        CURLOPT_PRIVATE        => $id,    // tag the handle so we know which ID finished
    ]);
    return $ch;
}

/**
 * Check every ID, keeping at most $concurrency requests in flight.
 * Calls $onResult(int $id, int $status) as each request finishes (in completion order).
 */
function checkIds(array $ids, int $concurrency, callable $onResult): void
{
    $mh       = curl_multi_init();
    $next     = 0;
    $inFlight = 0;

    $addNext = function () use ($mh, $ids, &$next, &$inFlight) {
        curl_multi_add_handle($mh, makeHandle($ids[$next++]));
        $inFlight++;
    };

    while ($inFlight < $concurrency && $next < count($ids)) {
        $addNext();
    }

    while ($inFlight > 0) {
        curl_multi_exec($mh, $running);
        if (curl_multi_select($mh, 1.0) === -1) {
            usleep(10_000); // select can return -1 immediately on some systems; avoid a busy loop
        }

        while ($info = curl_multi_info_read($mh)) {
            $ch = $info['handle'];
            $id = (int) curl_getinfo($ch, CURLINFO_PRIVATE);

            if ($info['result'] === CURLE_OK) {
                $status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
            } else {
                error_log("cURL error for $id: " . curl_strerror($info['result']));
                $status = 0;
            }

            curl_multi_remove_handle($mh, $ch);
            curl_close($ch);
            $inFlight--;

            $onResult($id, $status);

            // Refill the slot that just freed up.
            if ($next < count($ids)) {
                $addNext();
            }
        }
    }

    curl_multi_close($mh);
}

$start       = (int) ($argv[1] ?? 14695005);
$count       = (int) ($argv[2] ?? 10_000);
$concurrency = (int) ($argv[3] ?? 10);

// Requests finish out of order; buffer results so output stays in ID order.
$pending     = [];
$nextToPrint = $start;

checkIds(range($start, $start + $count - 1), $concurrency, function (int $id, int $status) use (&$pending, &$nextToPrint) {
    $pending[$id] = $status;
    while (isset($pending[$nextToPrint])) {
        echo $nextToPrint . ',' . $pending[$nextToPrint] . PHP_EOL;
        unset($pending[$nextToPrint]);
        $nextToPrint++;
    }
});
