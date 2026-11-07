<?php
/**
 * kamir.si – spletna različica čiščenja BMP slik (za gostovanje brez SSH).
 *
 * 1. Naloži to datoteko v public_html (poleg wp-load.php).
 * 2. Odpri https://kamir.si/kamir-bmp-web.php?key=KLJUČ&mode=status
 * 3. Po koncu: ?mode=selfdestruct izbriše to datoteko. Obvezno!
 *
 * Načini (parameter mode): status | convert | orphan-bmp | delete-orphan-bmp | delete-orphan-webp | purge | selfdestruct
 * Dodatni parametri: dry=1 (samo izpis), n=20 (velikost paketa pri convert)
 */
define( 'KAMIR_KEY', 'VPISI_DOLG_NAKLJUCEN_KLJUC' );

if ( ! isset( $_GET['key'] ) || ! hash_equals( KAMIR_KEY, (string) $_GET['key'] ) ) {
	http_response_code( 404 );
	exit( 'Not found' );
}

header( 'Content-Type: text/plain; charset=utf-8' );
header( 'X-Robots-Tag: noindex' );
header( 'X-LiteSpeed-Cache-Control: no-cache' );
@set_time_limit( 0 );
@ini_set( 'memory_limit', '512M' );
ignore_user_abort( true );
if ( function_exists( 'ini_set' ) ) { @ini_set( 'display_errors', '1' ); }

define( 'WP_USE_THEMES', false );
require __DIR__ . '/wp-load.php';
if ( ! function_exists( 'wp_generate_attachment_metadata' ) ) {
	require_once ABSPATH . 'wp-admin/includes/image.php';
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
}

$mode = isset( $_GET['mode'] ) ? preg_replace( '/[^a-z-]/', '', $_GET['mode'] ) : 'status';
$dry  = ! empty( $_GET['dry'] );
$n    = isset( $_GET['n'] ) ? max( 1, min( 200, (int) $_GET['n'] ) ) : 20;

$uploads = wp_upload_dir();
$basedir = trailingslashit( $uploads['basedir'] );
$baseurl = trailingslashit( $uploads['baseurl'] );
$freed   = 0;

function out( $s ) { echo $s, "\n"; @ob_flush(); @flush(); }
function webp_twin( $p ) { return preg_replace( '/\.bmp$/i', '.webp', $p ); }

/* Priponke, že izbrisane 7. 11. 2026 (ostane samo za varovalko). */
$unused_ids = array( 8927,8947,8974,8981,10326,10439,10514,10515,10516,10518,10519,10520,10521,10523,10524,10530,10531,10532,10533,10534,10535,10540,10541,10543,10570,10582,10584,11004,11006,11007,11009,11010,11338,11394,11395,11594,11642,11734,11736,11789,11916,11917,11918,11922,11923,11924,11930,11931,11932,11933,11948,11958,12049,12055,12056,12058,12060,12061,12206,12220,12258,12270,12293,12294,12454,12812,12813,13856 );

/* .webp dvojnice izbrisanih priponk. */
$orphan_webp = array(
	'2025/11/20251114191723060.webp',
	'2025/11/20251114191852670.webp',
	'2025/11/20251114192030853.webp',
	'2025/11/20251114192053510.webp',
	'2025/11/20251117123329297.webp',
	'2025/11/20251118134242107.webp',
	'2025/11/20251125091534333.webp',
	'2025/11/20251125091538453.webp',
	'2025/11/20251125094534763.webp',
	'2025/11/20251125094541733.webp',
	'2025/11/20251125094544983.webp',
	'2025/11/20251125094547993.webp',
	'2025/11/20251125094551667.webp',
	'2025/11/20251125094558870.webp',
	'2025/11/20251125094602877.webp',
	'2025/11/20251125101530393.webp',
	'2025/11/20251125101534240.webp',
	'2025/11/20251125101537520.webp',
	'2025/11/20251125101543550.webp',
	'2025/11/20251125101547547.webp',
	'2025/11/20251125101551610.webp',
	'2025/11/20251125101608743.webp',
	'2025/11/20251125101612640.webp',
	'2025/11/20251125101620527.webp',
	'2025/11/20251126084531453.webp',
	'2025/11/20251126104530720.webp',
	'2025/11/20251126104537517.webp',
	'2025/12/20251208094555827.webp',
	'2025/12/20251208094604293.webp',
	'2025/12/20251208094608223.webp',
	'2025/12/20251208094616150.webp',
	'2025/12/20251208094620970.webp',
	'2025/12/20251210083154680.webp',
	'2025/12/20251210144507770.webp',
	'2025/12/20251210145852577.webp',
	'2025/12/20251217141509590.webp',
	'2025/12/20251218141504567.webp',
	'2025/12/20251223111504367.webp',
	'2025/12/20251223111509867.webp',
	'2025/12/20251223134742160.webp',
	'2025/12/20251229114540603.webp',
	'2025/12/20251229114544117.webp',
	'2025/12/20251229114547667.webp',
	'2025/12/20251229121539583.webp',
	'2025/12/20251229121543510.webp',
	'2025/12/20251229121547240.webp',
	'2025/12/20251229123832340.webp',
	'2025/12/20251229123835740.webp',
	'2025/12/20251229123839580.webp',
	'2025/12/20251229123843460.webp',
	'2025/12/20251229131336647.webp',
	'2025/12/20251229131411950.webp',
	'2026/01/20260105134527680.webp',
	'2026/01/20260105141524947.webp',
	'2026/01/20260105141527970.webp',
	'2026/01/20260105141529490.webp',
	'2026/01/20260105141531400.webp',
	'2026/01/20260105141532123.webp',
	'2026/01/20260107091520733.webp',
	'2026/01/20260107101538447.webp',
	'2026/01/20260108134520577.webp',
	'2026/01/20260108151528440.webp',
	'2026/01/20260112111526270.webp',
	'2026/01/20260112111529513.webp',
	'2026/01/20260114101522653.webp',
	'2026/01/20260119084250543.webp',
	'2026/01/20260119084251750.webp',
	'2026/02/20260225142951277.webp',
);

function bmp_attachments() {
	return get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'any',
		'post_mime_type' => 'image/bmp',
		'fields'         => 'ids',
		'posts_per_page' => -1,
		'orderby'        => 'ID',
		'order'          => 'ASC',
	) );
}

out( "kamir-bmp-web mode=$mode" . ( $dry ? ' (suhi tek)' : '' ) . ' ' . date( 'c' ) );

switch ( $mode ) {

	case 'status':
		$ids = bmp_attachments();
		$sz  = 0;
		foreach ( $ids as $id ) { $f = get_attached_file( $id ); if ( $f && file_exists( $f ) ) { $sz += filesize( $f ); } }
		out( sprintf( 'BMP priponk v knjižnici: %d (%.0f MB)', count( $ids ), $sz / 1048576 ) );
		$ow = 0; foreach ( $orphan_webp as $r ) { if ( file_exists( $basedir . $r ) ) { $ow++; } }
		out( "osirotelih .webp dvojnic na disku: $ow / " . count( $orphan_webp ) );
		out( 'GD webp: ' . ( function_exists( 'imagewebp' ) ? 'da' : 'ne' ) . ', Imagick: ' . ( class_exists( 'Imagick' ) ? implode( ',', array_intersect( array( 'WEBP' ), Imagick::queryFormats( 'WEBP' ) ) ) ?: 'brez WEBP' : 'ne' ) );
		break;

	case 'convert':
		$ids  = array_values( array_diff( bmp_attachments(), $unused_ids ) );
		$todo = count( $ids );
		out( "$todo BMP priponk še za konverzijo; ta paket: " . min( $n, $todo ) );
		foreach ( array_slice( $ids, 0, $n ) as $id ) {
			$bmp = get_attached_file( $id );
			if ( ! $bmp || ! preg_match( '/\.bmp$/i', $bmp ) ) { out( "#$id: pripeta datoteka ni .bmp – preskočim." ); continue; }
			$webp = webp_twin( $bmp );
			$rel  = str_replace( $basedir, '', $webp );
			if ( ! file_exists( $webp ) ) { out( "#$id: ni .webp za " . str_replace( $basedir, '', $bmp ) . ' – preskočim.' ); continue; }
			out( ( $dry ? '[suho] ' : '' ) . "#$id -> $rel" );
			if ( $dry ) { $freed += file_exists( $bmp ) ? filesize( $bmp ) : 0; continue; }
			update_attached_file( $id, $webp );
			wp_update_post( array( 'ID' => $id, 'post_mime_type' => 'image/webp', 'guid' => $baseurl . $rel ) );
			$meta = wp_generate_attachment_metadata( $id, $webp );
			if ( empty( $meta ) || is_wp_error( $meta ) ) {
				$dim  = @getimagesize( $webp );
				$meta = array( 'file' => $rel, 'width' => $dim ? $dim[0] : 0, 'height' => $dim ? $dim[1] : 0, 'filesize' => filesize( $webp ), 'sizes' => array(), 'image_meta' => array() );
				out( "   opozorilo: pomanjšanih različic ni bilo mogoče ustvariti; shranjeni osnovni metapodatki." );
			}
			wp_update_attachment_metadata( $id, $meta );
			if ( file_exists( $bmp ) ) { $freed += filesize( $bmp ); @unlink( $bmp ); }
		}
		out( 'ostane: ' . max( 0, $todo - ( $dry ? 0 : min( $n, $todo ) ) ) );
		break;

	case 'orphan-bmp':
	case 'delete-orphan-bmp':
		global $wpdb;
		$del   = ( 'delete-orphan-bmp' === $mode ) && ! $dry;
		$known = array_flip( array_map( 'strtolower', $wpdb->get_col( "SELECT meta_value FROM {$wpdb->postmeta} WHERE meta_key = '_wp_attached_file' AND meta_value LIKE '%.bmp'" ) ) );
		$it    = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $basedir, FilesystemIterator::SKIP_DOTS ) );
		$cnt   = 0;
		foreach ( $it as $f ) {
			if ( ! preg_match( '/\.bmp$/i', $f->getFilename() ) ) { continue; }
			$rel = str_replace( '\\', '/', substr( $f->getPathname(), strlen( $basedir ) ) );
			if ( isset( $known[ strtolower( $rel ) ] ) ) { continue; }
			$cnt++;
			$like = '%' . $wpdb->esc_like( $f->getBasename( '.bmp' ) ) . '%';
			$refs = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_content LIKE %s", $like ) )
			      + (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_value LIKE %s", $like ) );
			$size = $f->getSize();
			if ( $refs ) { out( sprintf( 'OMENJENA v bazi (%d) – preskočim: %s (%.1f MB)', $refs, $rel, $size / 1048576 ) ); continue; }
			out( ( $del ? 'briši ' : '[seznam] ' ) . sprintf( '%s (%.1f MB)', $rel, $size / 1048576 ) );
			$freed += $size;
			if ( $del ) { @unlink( $f->getPathname() ); }
		}
		out( "$cnt .bmp datotek brez priponke." );
		break;

	case 'delete-orphan-webp':
		foreach ( $orphan_webp as $rel ) {
			$path = $basedir . $rel;
			if ( ! file_exists( $path ) ) { out( "ni je več: $rel" ); continue; }
			if ( file_exists( preg_replace( '/\.webp$/', '.bmp', $path ) ) ) { out( "$rel: .bmp še obstaja – preskočim." ); continue; }
			$att = get_posts( array( 'post_type' => 'attachment', 'post_status' => 'any', 'fields' => 'ids', 'posts_per_page' => 1, 'meta_key' => '_wp_attached_file', 'meta_value' => $rel ) );
			if ( $att ) { out( "$rel: ima priponko #{$att[0]} – preskočim." ); continue; }
			out( ( $dry ? '[suho] ' : '' ) . "briši $rel" );
			$freed += filesize( $path );
			if ( ! $dry ) { @unlink( $path ); }
		}
		break;

	case 'purge':
		do_action( 'litespeed_purge_all' );
		out( 'LiteSpeed cache: zahtevan purge all.' );
		break;

	case 'selfdestruct':
		@unlink( __FILE__ );
		out( file_exists( __FILE__ ) ? 'NAPAKA: datoteke ni bilo mogoče izbrisati – izbriši jo ročno!' : 'Skripta izbrisana.' );
		break;

	default:
		out( 'Neznan mode.' );
}

out( sprintf( 'Sproščeno v tem klicu: %.1f MB', $freed / 1048576 ) );
