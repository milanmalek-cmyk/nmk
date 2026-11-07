<?php
/**
 * kamir.si – čiščenje BMP slik v medijski knjižnici.
 *
 * Zagon na strežniku (v korenu WordPressa) z WP-CLI:
 *
 *   wp eval-file kamir-bmp-cleanup.php dry-run                 # samo izpiše, kaj bi naredil
 *   wp eval-file kamir-bmp-cleanup.php delete-orphan-webp      # izbriše osirotele .webp dvojnice 68 že izbrisanih BMP priponk
 *   wp eval-file kamir-bmp-cleanup.php convert                 # priponke v uporabi preusmeri na .webp in izbriše .bmp
 *   wp eval-file kamir-bmp-cleanup.php convert dry-run         # kombinacija: konverzija samo na suho
 *   wp eval-file kamir-bmp-cleanup.php orphan-bmp                 # izpiše .bmp datoteke v uploads, ki niso v medijski knjižnici
 *   wp eval-file kamir-bmp-cleanup.php delete-orphan-bmp          # ... in jih izbriše (če jih nič v bazi ne omenja)
 *
 * 68 neuporabljenih BMP priponk je bilo 7. 11. 2026 že izbrisanih prek REST API-ja (priponka + .bmp).
 * Njihove .webp dvojnice so ostale na disku, ker jih WordPress ob brisanju priponke ne pozna.
 *
 * Pred zagonom naredi varnostno kopijo baze in mape wp-content/uploads!
 * Po zagonu počisti LiteSpeed Cache: wp litespeed-purge all
 */

if ( ! defined( 'WP_CLI' ) || ! WP_CLI ) {
	die( "Zaženi z WP-CLI: wp eval-file kamir-bmp-cleanup.php <delete-orphan-webp|convert> [dry-run]\n" );
}

$dry_run       = in_array( 'dry-run', $args, true );
$delete_orphan = in_array( 'delete-orphan-webp', $args, true );
$convert       = in_array( 'convert', $args, true );
$orphan_bmp    = in_array( 'orphan-bmp', $args, true ) || in_array( 'delete-orphan-bmp', $args, true );
$orphan_delete = in_array( 'delete-orphan-bmp', $args, true ) && ! $dry_run;

if ( ! $delete_orphan && ! $convert && ! $orphan_bmp && ! $dry_run ) {
	WP_CLI::error( 'Podaj način: delete-orphan-webp, convert, orphan-bmp, delete-orphan-bmp ali dry-run.' );
}
if ( $dry_run && ! $delete_orphan && ! $convert ) {
	$delete_orphan = true;
	$convert       = true;
}

/*
 * Priponke BMP, ki 7. 11. 2026 niso bile niti glavna niti galerijska slika
 * nobenega izdelka (tudi osnutkov in zasebnih ne) in se njihovo ime ne pojavi
 * na nobeni strani (glej bmp-neuporabljene.csv). Izbrisane prek REST API-ja;
 * seznam ostaja, da jih način convert zanesljivo preskoči.
 */
$unused_ids = array(
	8927, 8947, 8974, 8981, 10326, 10439, 10514, 10515, 10516, 10518, 10519, 10520, 10521,
	10523, 10524, 10530, 10531, 10532, 10533, 10534, 10535, 10540, 10541, 10543, 10570, 10582,
	10584, 11004, 11006, 11007, 11009, 11010, 11338, 11394, 11395, 11594, 11642, 11734, 11736,
	11789, 11916, 11917, 11918, 11922, 11923, 11924, 11930, 11931, 11932, 11933, 11948, 11958,
	12049, 12055, 12056, 12058, 12060, 12061, 12206, 12220, 12258, 12270, 12293, 12294, 12454,
	12812, 12813, 13856,
);

$uploads  = wp_upload_dir();
$basedir  = trailingslashit( $uploads['basedir'] );
$baseurl  = trailingslashit( $uploads['baseurl'] );
$freed    = 0;

function kamir_webp_twin( $bmp_path ) {
	return preg_replace( '/\.bmp$/i', '.webp', $bmp_path );
}

/* ---------- 1) Brisanje osirotelih .webp dvojnic že izbrisanih priponk ---------- */
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

if ( $delete_orphan ) {
	WP_CLI::log( '== Osirotele .webp dvojnice (68 izbrisanih BMP priponk) ==' );
	foreach ( $orphan_webp as $rel ) {
		$path = $basedir . $rel;
		$bmp  = preg_replace( '/\.webp$/', '.bmp', $path );
		if ( ! file_exists( $path ) ) {
			WP_CLI::log( "ni je več: $rel" );
			continue;
		}
		// Varovalka: če .bmp še obstaja ali ima .webp svojo priponko, je ne brišemo.
		if ( file_exists( $bmp ) ) {
			WP_CLI::warning( "$rel: .bmp original še obstaja – preskočim." );
			continue;
		}
		$att = get_posts( array( 'post_type' => 'attachment', 'post_status' => 'any', 'fields' => 'ids', 'posts_per_page' => 1, 'meta_key' => '_wp_attached_file', 'meta_value' => $rel ) );
		if ( $att ) {
			WP_CLI::warning( "$rel: ima priponko #{$att[0]} – preskočim." );
			continue;
		}
		WP_CLI::log( ( $dry_run ? '[suho] ' : '' ) . "briši $rel" );
		$freed += filesize( $path );
		if ( ! $dry_run ) {
			@unlink( $path );
		}
	}
}

/* ---------- 2) Konverzija priponk v uporabi: .bmp -> .webp ---------- */
if ( $convert ) {
	WP_CLI::log( '== BMP priponke v uporabi -> preusmeritev na .webp ==' );
	$ids = get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'any',
		'post_mime_type' => 'image/bmp',
		'fields'         => 'ids',
		'posts_per_page' => -1,
	) );
	$ids = array_diff( $ids, $unused_ids );
	WP_CLI::log( count( $ids ) . ' priponk za konverzijo.' );

	foreach ( $ids as $id ) {
		$bmp = get_attached_file( $id );
		if ( ! $bmp || ! preg_match( '/\.bmp$/i', $bmp ) ) {
			WP_CLI::warning( "#$id: pripeta datoteka ni .bmp ($bmp) – preskočim." );
			continue;
		}
		$webp = kamir_webp_twin( $bmp );
		if ( ! file_exists( $webp ) ) {
			WP_CLI::warning( "#$id: ni .webp dvojnice za " . str_replace( $basedir, '', $bmp ) . ' – preskočim (BMP ostane).' );
			continue;
		}
		$rel_webp = str_replace( $basedir, '', $webp );
		WP_CLI::log( ( $dry_run ? '[suho] ' : '' ) . "#$id -> $rel_webp, briši .bmp" );
		if ( $dry_run ) {
			$freed += file_exists( $bmp ) ? filesize( $bmp ) : 0;
			continue;
		}

		// Priponka naj kaže na .webp.
		update_attached_file( $id, $webp );
		wp_update_post( array(
			'ID'             => $id,
			'post_mime_type' => 'image/webp',
			'guid'           => $baseurl . $rel_webp,
		) );

		// Metapodatki + pomanjšane različice (BMP jih ni imel).
		$meta = wp_generate_attachment_metadata( $id, $webp );
		if ( empty( $meta ) || is_wp_error( $meta ) ) {
			$dim  = @getimagesize( $webp );
			$meta = array( 'file' => $rel_webp, 'width' => $dim ? $dim[0] : 0, 'height' => $dim ? $dim[1] : 0, 'filesize' => filesize( $webp ), 'sizes' => array(), 'image_meta' => array() );
			WP_CLI::warning( "#$id: pomanjšanih različic ni bilo mogoče ustvariti (strežnik brez WebP podpore v GD/Imagick?) – shranjeni osnovni metapodatki." );
		}
		wp_update_attachment_metadata( $id, $meta );

		if ( file_exists( $bmp ) ) {
			$freed += filesize( $bmp );
			@unlink( $bmp );
		}
	}
}

/* ---------- 3) BMP datoteke na disku, ki niso v medijski knjižnici ---------- */
if ( $orphan_bmp ) {
	global $wpdb;
	WP_CLI::log( '== .bmp datoteke v uploads brez priponke ==' );
	$known = $wpdb->get_col( "SELECT meta_value FROM {$wpdb->postmeta} WHERE meta_key = '_wp_attached_file' AND meta_value LIKE '%.bmp'" );
	$known = array_flip( array_map( 'strtolower', $known ) );
	$it    = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $basedir, FilesystemIterator::SKIP_DOTS ) );
	$n     = 0;
	foreach ( $it as $f ) {
		if ( ! preg_match( '/\.bmp$/i', $f->getFilename() ) ) {
			continue;
		}
		$rel = str_replace( '\\', '/', substr( $f->getPathname(), strlen( $basedir ) ) );
		if ( isset( $known[ strtolower( $rel ) ] ) ) {
			continue; // ima priponko – obravnava jo način convert
		}
		$n++;
		$base = $f->getBasename( '.bmp' );
		// Ali ime datoteke kje v bazi še omenjeno (vsebina, Elementor, meta)?
		$like = '%' . $wpdb->esc_like( $base ) . '%';
		$refs = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_content LIKE %s", $like ) )
		      + (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_value LIKE %s", $like ) );
		$size = $f->getSize();
		if ( $refs ) {
			WP_CLI::warning( sprintf( '%s (%.1f MB): brez priponke, a omenjena %d-krat v bazi – preskočim.', $rel, $size / 1048576, $refs ) );
			continue;
		}
		WP_CLI::log( ( $orphan_delete ? 'briši ' : '[seznam] ' ) . sprintf( '%s (%.1f MB)', $rel, $size / 1048576 ) );
		$freed += $size;
		if ( $orphan_delete ) {
			@unlink( $f->getPathname() );
		}
	}
	WP_CLI::log( "$n .bmp datotek brez priponke." );
}

WP_CLI::success( sprintf( '%s Sproščeno: %.1f MB', $dry_run ? '(suhi tek)' : 'Končano.', $freed / 1048576 ) );
if ( ! $dry_run ) {
	WP_CLI::log( 'Zdaj počisti predpomnilnik: wp litespeed-purge all' );
}
